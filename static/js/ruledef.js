// $(document).ready(function () {
//   $("select")
//     .change(function () {
//       $(this)
//         .find("option:selected")
//         .each(function () {
//           var optionValue = $(this).attr("value");
//           if (optionValue) {
//             $(".box")
//               .not("." + optionValue)
//               .hide();
//             $("." + optionValue).show();
//           } else {
//             $(".box").hide();
//           }
//         });
//     })
//     .change();
// });

// $(document).ready(function () {
//   $(".delete").hide();
//   //when the Add Field button is clicked
//   $("#add").click(function (e) {
//     $(".delete").fadeIn("1500");
//     //Append a new row of code to the "#items" div
//     $("#items").append(
//       '<div class="next-referval col-8 mb-1"><input id="textinput" name="textinput" type="text" placeholder="Enter Reference Value" class="form-control input-md"></div>'
//     );
//   });
//   $("body").on("click", ".delete", function (e) {
//     $(".next-referval").last().remove();
//   });
// });

// function hideDiv() {
//   var v = document.getElementById("matcher_div");
//   if (v.style.display != "none") {
//     v.style.display = "none";
//   }
// }

