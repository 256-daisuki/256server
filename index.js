//sp menu

(function () {
    document
      .querySelector("body")
      .insertAdjacentHTML("afterbegin", '<div class="sp-navi-box"><div class="sp-navi"></div></div>');
    document.querySelector(".sp-navi").innerHTML = document.querySelector(
      ".navi"
    ).innerHTML;
  
    const documentElement = document.querySelector("html");
    const contentElement = document.querySelector("#main");
    const sidebarElement = document.querySelector(".sp-navi-box");
    const openSidebar = function () {
      scl_point = window.pageYOffset;
      documentElement.classList.add("sidebar-is-open");
      $("body").css("top", "-" + scl_point + "px");
    };
    const closeSidebar = function () {
      documentElement.classList.remove("sidebar-is-open");
      $(window).scrollTop(
        $("body").css("top").replace(/-/g, "").replace(/px/g, "")
      );
      $("body").css("top", 0);
    };
    $(".sp-navi-toggle").click(function () {
      //, .sp-navi-box a[href^=#]
      if ($(".sidebar-is-open").length) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  })();