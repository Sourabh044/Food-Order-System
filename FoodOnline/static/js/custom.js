let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      //default in this app is "IN" - add your country code
      componentRestrictions: { country: ["in"] },
    }
  );
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    console.log("place name=>", place.name);
  }
  // get the address components and assign them to the fields
}

$(document).ready(function () {
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data-id");
    console.log(food_id);
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/login-user";
          });
        } else if (response.status == false) {
          swal(response.message, "", "error");
          console.log(response);
        } else {
          // console.log(response)
          // swal(response.message,'','success')
          $("#cart_count").html(response["cart_count"].cart_count);
          $("#qty-" + food_id).html(response.qty);
          console.log(response);
          applyCartAmounts(
            response.cart_amount.subtotal,
            response.cart_amount.tax,
            response.cart_amount.total
          );
        }
        // $('#cart_count').html(response['cart_count'].cart_count)
        // $('#qty-'+food_id).html(response.qty)
      },
    });
  });

  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data-qty");
    $("#" + the_id).html(qty);
  });

  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data-id");
    url = $(this).attr("data-url");

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/login-user";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          if (response["qty"] == 0) {
            location.reload(true);
            $("#qty-" + food_id).html(response.qty);
            applyCartAmounts(
              response.cart_amount.subtotal,
              response.cart_amount.tax,
              response.cart_amount.total
            );
            document.getElementById().remove();
          } else {
            $("#cart_count").html(response["cart_count"].cart_count);
            $("#qty-" + food_id).html(response.qty);
            applyCartAmounts(
              response.cart_amount.subtotal,
              response.cart_amount.tax,
              response.cart_amount.total
            );
          }
        }
      },
    });
  });

  $(".delete_cart").on("click", function (e) {
    e.preventDefault();

    cart_id = $(this).attr("data-id");
    url = $(this).attr("data-url");
    // swal(cart_id,'','info')
    // return false

    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status == "login_required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/login-user";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          console.log(response);
          if (typeof cart_count === "undefined" && cart_count === undefined) {
            $("#cart_count").html(response["cart_count"].cart_count);
            applyCartAmounts(
              response.cart_amount.subtotal,
              response.cart_amount.tax,
              response.cart_amount.total
            );
          }
          swal(response.message, "", "info").then(function () {
            location.reload(true);
            console.log(response);
            applyCartAmounts(
              response.cart_amount.subtotal,
              response.cart_amount.tax,
              response.cart_amount.total
            );
          });
        }
      },
    });
  });

  function applyCartAmounts(subtotal, tax, total) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);
      $("#tax").html(tax);
      $("#total").html(total);
    }
  }
});
(function ($) {
  $(document).on("google_point_map_widget:marker_create", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log("EVENT: marker_create"); // django widget textarea widget (hidden)
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng); // created marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
  });

  $(document).on("google_point_map_widget:marker_change", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log("EVENT: marker_change"); // django widget textarea widget (hidden)
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng);  // changed marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
  });

  $(document).on("google_point_map_widget:marker_delete", function (e, lat, lng, locationInputElem, mapWrapID) {
    console.log("EVENT: marker_delete"); // django widget textarea widget (hidden)
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng);  // deleted marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
  })

  $(document).on("google_point_map_widget:place_changed", function (e, place, lat, lng, locationInputElem, mapWrapID) {
    console.log("EVENT: place_changed"); // django widget textarea widget (hidden)
    console.log(place);  // google geocoder place object
    console.log(locationInputElem); // django widget textarea widget (hidden)
    console.log(lat, lng); // created marker coordinates
    console.log(mapWrapID); // map widget wrapper element ID
  });
})(jQuery)