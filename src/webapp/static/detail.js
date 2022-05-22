function toggle() {
  let bts = document.getElementsByClassName("button");
  for (let btn of bts) {
    if (btn.classList.contains("button-green")) {
      btn.classList.remove("button-green");
      btn.classList.add("button-red");
      btn.innerHTML = "Quit CoLearn Space";
    } else {
      btn.classList.remove("button-red");
      btn.classList.add("button-green");
      btn.innerHTML = "Join CoLearn Space";
    }
  }
}

$(".button").click(function () {
  var slug;
  slug = $(this).attr("data-slug");
  $.ajax({
    type: "GET",
    url: `/detail/${slug}/Favourites`,
    success: function (data) {
      console.log("Success");
    },
  });
});