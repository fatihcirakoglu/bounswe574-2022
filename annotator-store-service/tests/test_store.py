from . import TestCase
from .helpers import MockUser
from nose.tools import *
from mock import patch

from flask import json, g
from six.moves import xrange

from annotator import auth, es
from annotator.annotation import Annotation


class TestStore(TestCase):
    def setup(self):
        super(TestStore, self).setup()

        self.user = MockUser()

        payload = {'consumerKey': self.user.consumer.key, 'userId': self.user.id}
        token = auth.encode_token(payload, self.user.consumer.secret)
        self.headers = {'x-annotator-auth-token': token}

        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def teardown(self):
        self.ctx.pop()
        super(TestStore, self).teardown()

    def _create_annotation(self, refresh=True, **kwargs):
        opts = {
            'user': self.user.id,
            'consumer': self.user.consumer.key
        }
        opts.update(kwargs)
        ann = Annotation(**opts)
        ann.save(refresh=refresh)
        return ann

    def _get_annotation(self, id_):
        return Annotation.fetch(id_)

    def test_cors_preflight(self):
        response = self.cli.open('/api/annotations', method="OPTIONS")

        headers = dict(response.headers)

        assert headers['Access-Control-Allow-Methods'] == 'GET, POST, PUT, DELETE, OPTIONS', \
            "Did not send the right Access-Control-Allow-Methods header."

        assert headers['Access-Control-Allow-Origin'] == '*', \
            "Did not send the right Access-Control-Allow-Origin header."

        assert headers['Access-Control-Expose-Headers'] == 'Content-Length, Content-Type, Location', \
            "Did not send the right Access-Control-Expose-Headers header."

    @patch('annotator.store.Annotation')
    def test_pluggable_class(self, ann_mock):
        g.annotation_class = ann_mock
        response = self.cli.get('/api/annotations/testID', headers=self.headers)
        ann_mock.return_value.fetch.assert_called_once()

    def test_index(self):
        response = self.cli.get('/api/annotations', headers=self.headers)
        assert response.data == b"[]", "response should be empty list"

    def test_create(self):
        payload = json.dumps({'name': 'Foo'})

        response = self.cli.post('/api/annotations',
                                 data=payload,
                                 content_type='application/json',
                                 headers=self.headers)

        assert response.status_code == 201, "response should be 201 CREATED"
        data = json.loads(response.data)
        assert 'id' in data, "annotation id should be returned in response"
        expected_location = '/api/annotations/{0}'.format(data['id'])
        assert response.location.endswith(expected_location), (
            "The response should have a Location header with the URL to read "
            "the annotation that was created")
        assert data['user'] == self.user.id
        assert data['consumer'] == self.user.consumer.key

    def test_create_ignore_created(self):
        payload = json.dumps({'created': 'abc'})

        response = self.cli.post('/api/annotations',
                                 data=payload,
                                 content_type='application/json',
                                 headers=self.headers)

        data = json.loads(response.data)
        ann = self._get_annotation(data['id'])

        assert ann['created'] != 'abc', "annotation 'created' field should not be used by API"

    def test_create_ignore_updated(self):
        payload = json.dumps({'updated': 'abc'})

        response = self.cli.post('/api/annotations',
                                 data=payload,
                                 content_type='application/json',
                                 headers=self.headers)

        data = json.loads(response.data)
        ann = self._get_annotation(data['id'])

        assert ann['updated'] != 'abc', "annotation 'updated' field should not be used by API"

    def test_create_ignore_auth_in_payload(self):
        payload = json.dumps({'user': 'jenny', 'consumer': 'myconsumer'})

        response = self.cli.post('/api/annotations',
                                 data=payload,
                                 content_type='application/json',
                                 headers=self.headers)

        data = json.loads(response.data)
        ann = self._get_annotation(data['id'])

        assert ann['user'] == self.user.id, "annotation 'user' field should not be futzable by API"
        assert ann['consumer'] == self.user.consumer.key, "annotation 'consumer' field should not be used by API"

    def test_create_should_not_update(self):
        response = self.cli.post('/api/annotations',
                                 data=json.dumps({'name': 'foo'}),
                                 content_type='application/json',
                                 headers=self.headers)
        data = json.loads(response.data)
        id_ = data['id']

        # Try and update the annotation using the create API
        response = self.cli.post('/api/annotations',
                                 data=json.dumps({'name': 'bar', 'id': id_}),
                                 content_type='application/json',
                                 headers=self.headers)
        data = json.loads(response.data)


        assert id_ != data['id'], "create should always create a new annotation"

        ann1 = self._get_annotation(id_)
        ann2 = self._get_annotation(data['id'])

        assert ann1['name'] == 'foo', "annotation name should be 'foo'"
        assert ann2['name'] == 'bar', "annotation name should be 'bar'"

    @patch('annotator.store.json')
    @patch('annotator.store.Annotation')
    def test_create_refresh(self, ann_mock, json_mock):
        json_mock.dumps.return_value = "{}"
        response = self.cli.post('/api/annotations?refresh=true',
                                 data="{}",
                                 content_type='application/json',
                                 headers=self.headers)
        ann_mock.return_value.save.assert_called_once_with(refresh=True)

    @patch('annotator.store.json')
    @patch('annotator.store.Annotation')
    def test_create_disable_refresh(self, ann_mock, json_mock):
        json_mock.dumps.return_value = "{}"
        response = self.cli.post('/api/annotations?refresh=false',
                                 data="{}",
                                 content_type='application/json',
                                 headers=self.headers)
        ann_mock.return_value.save.assert_called_once_with(refresh=False)

    def test_read(self):
        kwargs = dict(text=u"Foo", id='123')
        self._create_annotation(**kwargs)
        response = self.cli.get('/api/annotations/123', headers=self.headers)
        data = json.loads(response.data)
        assert data['id'] == '123', "annotation id should be returned in response"
        assert data['text'] == "Foo", "annotation text should be returned in response"

    def test_read_notfound(self):
        response = self.cli.get('/api/annotations/123', headers=self.headers)
        assert response.status_code == 404, "response should be 404 NOT FOUND"

    def test_update(self):
        self._create_annotation(text=u"Foo", id='123', created='2010-12-10')

        payload = json.dumps({'id': '123', 'text': 'Bar'})
        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.headers)

        ann = self._get_annotation('123')
        assert ann['text'] == "Bar", "annotation wasn't updated in db"

        data = json.loads(response.data)
        assert data['text'] == "Bar", "update annotation should be returned in response"

    def test_update_without_payload_id(self):
        self._create_annotation(text=u"Foo", id='123')

        payload = json.dumps({'text': 'Bar'})
        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.headers)

        ann = self._get_annotation('123')
        assert ann['text'] == "Bar", "annotation wasn't updated in db"

    def test_update_with_wrong_payload_id(self):
        self._create_annotation(text=u"Foo", id='123')

        payload = json.dumps({'text': 'Bar', 'id': 'abc'})
        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.headers)

        ann = self._get_annotation('123')
        assert ann['text'] == "Bar", "annotation wasn't updated in db"

    def test_update_notfound(self):
        response = self.cli.put('/api/annotations/123', headers=self.headers)
        assert response.status_code == 404, "response should be 404 NOT FOUND"

    def test_update_ignore_created(self):
        ann = self._create_annotation(text=u"Foo", id='123')

        payload = json.dumps({'created': 'abc'})

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.headers)

        upd = self._get_annotation('123')

        assert upd['created'] == ann['created'], "annotation 'created' field should not be updated by API"

    def test_update_ignore_updated(self):
        ann = self._create_annotation(text=u"Foo", id='123')

        payload = json.dumps({'updated': 'abc'})

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.headers)

        upd = self._get_annotation('123')

        assert upd['created'] != 'abc', "annotation 'updated' field should not be updated by API"

    def test_update_ignore_auth_in_payload(self):
        ann = self._create_annotation(text=u"Foo", id='123')

        payload = json.dumps({'user': 'jenny', 'consumer': 'myconsumer'})

        response = self.cli.put('/api/annotations/123',
                                 data=payload,
                                 content_type='application/json',
                                 headers=self.headers)

        upd = self._get_annotation('123')

        assert_equal(upd['user'], self.user.id, "annotation 'user' field should not be futzable by API")
        assert_equal(upd['consumer'], self.user.consumer.key, "annotation 'consumer' field should not be futzable by API")

    def test_delete(self):
        kwargs = dict(text=u"Bar", id='456')
        ann = self._create_annotation(**kwargs)

        response = self.cli.delete('/api/annotations/456', headers=self.headers)
        assert response.status_code == 204, "response should be 204 NO CONTENT"

        assert self._get_annotation('456') == None, "annotation wasn't deleted in db"

    def test_delete_notfound(self):
        response = self.cli.delete('/api/annotations/123', headers=self.headers)
        assert response.status_code == 404, "response should be 404 NOT FOUND"

    def test_search(self):
        uri1 = u'http://xyz.com'
        uri2 = u'urn:uuid:xxxxx'
        user = u'levin'
        user2 = u'anna'
        anno = self._create_annotation(uri=uri1, text=uri1, user=user)
        anno2 = self._create_annotation(uri=uri1, text=uri1 + uri1, user=user2)
        anno3 = self._create_annotation(uri=uri2, text=uri2, user=user)

        res = self._get_search_results()
        assert_equal(res['total'], 3)

        res = self._get_search_results('limit=1')
        assert_equal(res['total'], 3)
        assert_equal(len(res['rows']), 1)

        res = self._get_search_results('uri=' + uri1)
        assert_equal(res['total'], 2)
        assert_equal(len(res['rows']), 2)
        assert_equal(res['rows'][0]['uri'], uri1)
        assert_true(res['rows'][0]['id'] in [anno['id'], anno2['id']])

    def test_search_sort_and_order(self):
        uri1 = u'http://xyz.com'
        uri2 = u'urn:uuid:xxxxx'
        user = u'levin'
        user2 = u'anna'
        anno = self._create_annotation(uri=uri1, text=uri1, user=user)
        anno2 = self._create_annotation(uri=uri1, text=uri1 + uri1, user=user2)
        anno3 = self._create_annotation(uri=uri2, text=uri2, user=user)

        res = self._get_search_results('limit=1&sort=user&order=asc')
        assert_equal(res['total'], 3)
        assert_equal(len(res['rows']), 1)
        assert_equal(res['rows'][0]['user'], user2)

        res = self._get_search_results('limit=1&sort=user&order=desc')
        assert_equal(res['total'], 3)
        assert_equal(len(res['rows']), 1)
        assert_equal(res['rows'][0]['user'], user)

        res = self._get_search_results('limit=1&sort=text&user=' + user)
        assert_equal(res['total'], 2)
        assert_equal(len(res['rows']), 1)
        assert_equal(res['rows'][0]['text'], anno['text'])

    def test_search_limit(self):
        for i in xrange(250):
            self._create_annotation(refresh=False)

        es.conn.indices.refresh(es.index)

        # by default return 20
        res = self._get_search_results()
        assert_equal(len(res['rows']), 20)

        # return maximum 200
        res = self._get_search_results('limit=250')
        assert_equal(len(res['rows']), 200)

        # return minimum 0
        res = self._get_search_results('limit=-10')
        assert_equal(len(res['rows']), 0)

        # ignore bogus values
        res = self._get_search_results('limit=foobar')
        assert_equal(len(res['rows']), 20)

    def test_search_offset(self):
        for i in xrange(250):
            self._create_annotation(refresh=False)

        es.conn.indices.refresh(es.index)

        res = self._get_search_results()
        assert_equal(len(res['rows']), 20)
        first = res['rows'][0]

        res = self._get_search_results('offset=240')
        assert_equal(len(res['rows']), 10)

        # ignore negative values
        res = self._get_search_results('offset=-10')
        assert_equal(len(res['rows']), 20)
        assert_equal(res['rows'][0], first)

        # ignore bogus values
        res = self._get_search_results('offset=foobar')
        assert_equal(len(res['rows']), 20)
        assert_equal(res['rows'][0], first)

    def _get_search_results(self, qs=''):
        res = self.cli.get('/api/search?{qs}'.format(qs=qs), headers=self.headers)
        return json.loads(res.data)


class TestStoreAuthz(TestCase):

    def setup(self):
        super(TestStoreAuthz, self).setup()

        self.user = MockUser() # alice

        self.anno_id = '123'
        self.permissions = {
            'read': [self.user.id, 'bob'],
            'update': [self.user.id, 'charlie'],
            'admin': [self.user.id]
        }

        self.ctx = self.app.test_request_context()
        self.ctx.push()

        ann = Annotation(id=self.anno_id,
                         user=self.user.id,
                         consumer=self.user.consumer.key,
                         text='Foobar',
                         permissions=self.permissions)
        ann.save()

        for u in ['alice', 'bob', 'charlie']:
            token = auth.encode_token({'consumerKey': self.user.consumer.key, 'userId': u}, self.user.consumer.secret)
            setattr(self, '%s_headers' % u, {'x-annotator-auth-token': token})

    def teardown(self):
        self.ctx.pop()
        super(TestStoreAuthz, self).teardown()

    def test_index(self):
        # Test unauthenticated
        response = self.cli.get('/api/annotations')
        results = json.loads(response.data)
        assert results == [], "unauthenticated user should get an empty list"

        # Test as bob (authorized to read)
        response = self.cli.get('/api/annotations',
                           headers=self.bob_headers)
        results = json.loads(response.data)
        assert results and results[0]['id'] == self.anno_id, "bob should see his own annotation"

        # Test as charlie (unauthorized)
        response = self.cli.get('/api/annotations',
                           headers=self.charlie_headers)
        results = json.loads(response.data)
        assert results == []

    def test_read(self):
        response = self.cli.get('/api/annotations/123')
        assert response.status_code == 401, "response should be 401 NOT AUTHORIZED"

        response = self.cli.get('/api/annotations/123', headers=self.charlie_headers)
        assert response.status_code == 403, "response should be 403 FORBIDDEN"

        response = self.cli.get('/api/annotations/123', headers=self.alice_headers)
        assert response.status_code == 200, "response should be 200 OK"
        data = json.loads(response.data)
        assert data['text'] == 'Foobar'

    def test_update(self):
        payload = json.dumps({'id': self.anno_id, 'text': 'Bar'})

        response = self.cli.put('/api/annotations/123', data=payload, content_type='application/json')
        assert response.status_code == 401, "response should be 401 NOT AUTHORIZED"

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.bob_headers)
        assert response.status_code == 403, "response should be 403 FORBIDDEN"

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.charlie_headers)
        assert response.status_code == 200, "response should be 200 OK"

    def test_update_change_permissions_not_allowed(self):
        self.permissions['read'] = ['alice', 'charlie']
        payload = json.dumps({
            'id': self.anno_id,
            'text': 'Bar',
            'permissions': self.permissions
        })

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json')
        assert response.status_code == 401, "response should be 401 NOT AUTHORIZED"

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.charlie_headers)
        assert response.status_code == 403, "response should be 403 FORBIDDEN"
        assert b'permissions update' in response.data

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.alice_headers)
        assert response.status_code == 200, "response should be 200 OK"

    def test_update_other_users_annotation(self):
        ann = Annotation(id=123,
                         user='foo',
                         consumer=self.user.consumer.key,
                         permissions={'update': ['group:__consumer__']})
        ann.save()

        payload = json.dumps({
            'id': 123,
            'text': 'Foo'
        })

        response = self.cli.put('/api/annotations/123',
                                data=payload,
                                content_type='application/json',
                                headers=self.bob_headers)
        assert response.status_code == 200, "response should be 200 OK"

    def test_search_public(self):
        # Not logged in: no results
        results = self._get_search_results()
        assert results['total'] == 0
        assert results['rows'] == []

    def test_search_authenticated(self):
        # Logged in as Bob: 1 result
        results = self._get_search_results(headers=self.bob_headers)
        assert results['total'] == 1
        assert results['rows'][0]['id'] == self.anno_id

        # Logged in as Charlie: 0 results
        results = self._get_search_results(headers=self.charlie_headers)
        assert results['total'] == 0
        assert results['rows'] == []

    def test_search_raw_public(self):
        # Not logged in: no results
        results = self._get_search_raw_results()
        assert results['hits']['total'] == 0
        assert results['hits']['hits'] == []

    def test_search_raw_authorized(self):
        # Logged in as Bob: 1 result
        results = self._get_search_raw_results(headers=self.bob_headers)
        assert results['hits']['total'] == 1
        assert results['hits']['hits'][0]['_id'] == self.anno_id

        # Logged in as Charlie: 0 results
        results = self._get_search_raw_results(headers=self.charlie_headers)
        assert results['hits']['total'] == 0
        assert results['hits']['hits'] == []

    def _get_search_results(self, qs='', **kwargs):
        res = self.cli.get('/api/search?{qs}'.format(qs=qs), **kwargs)
        return json.loads(res.data)

    def _get_search_raw_results(self, qs='', **kwargs):
        res = self.cli.get('/api/search_raw?{qs}'.format(qs=qs), **kwargs)
        return json.loads(res.data)
