// Select2
$(document).ready(function () {
	$(".js-example-basic-single").select2();
});

// $(function () {
//   $("table.table1 tr").click(function () {
//     window.location.href = $(this).data("url");
//   });
// });

// Currenly active link in navbar
var btnContainer = document.getElementById("sidebar");

if (btnContainer) {
	var btns = btnContainer.getElementsByClassName("nav-link");

	for (var i = 0; i < btns.length; i++) {
		btns[i].addEventListener("click", function () {
			var current = document.getElementsByClassName("active");
			current[0].className = current[0].className.replace(" active", "");
			this.className += " active";
		});
	}
}

function display_array() {
	var e = "<hr/>";

	for (var y = 0; y < array.length; y++) {
		e += "Element " + y + " = " + array[y] + "<br/>";
	}
	document.getElementById("Result").innerHTML = e;
}
//Counter to maintain number of textboxes and give them unique id for later reference
var intTextBox = 0;

/**
 * Function to add textbox element dynamically
 * First we incrementing the counter and creating new div element with unique id
 * Then adding new textbox element to this div and finally appending this div to main content.
 */
function addElement() {
	intTextBox++;
	var objNewDiv = document.createElement("div");
	objNewDiv.setAttribute("id", "div_" + intTextBox);
	objNewDiv.innerHTML =
		"Textbox " +
		intTextBox +
		': <input type="text" id="tb_' +
		intTextBox +
		'" name="tb_' +
		intTextBox +
		'"/>';
	document.getElementById("content").appendChild(objNewDiv);
}

/**
 * Function to remove textbox element dynamically
 * check if counter is more than zero then remove the div element with the counter id and reduce the counter
 * if counter is zero then show alert as no existing textboxes are there
 */
function removeElement() {
	if (0 < intTextBox) {
		document
			.getElementById("content")
			.removeChild(document.getElementById("div_" + intTextBox));
		intTextBox--;
	} else {
		alert("No textbox to remove");
	}
}

var $select1 = $("#select1"),
	$select2 = $("#select2"),
	$select3 = $("#select3"),
	$select4 = $("#select4"),
	$select5 = $("#select5"),
	$select6 = $("#select6"),
	$option2 = $select2.find("option"),
	$option3 = $select3.find("option"),
	$option4 = $select4.find("option"),
	$option5 = $select5.find("option");

$select1.on("change", function () {
	$select2.html($option2.filter('[value="' + this.value + '"]'));
	$select3.html($option3.filter('[value="' + this.value + '"]'));
	$select4.html($option4.filter('[value="' + this.value + '"]'));
	$select5.html($option5.filter('[value="' + this.value + '"]'));
});

$select6.on("change", function () {
	value = $("#select6 :selected").val(); // The value of the selected option
	$("#exampleModalLabel").text(value);
});
// Select2
$(document).ready(function () {
	$("#cname").select2();
	$("#select1").select2();
	$("#select2").select2();
	$("#select3").select2();
	$("#select4").select2();
	$("#select5").select2();
	$("#select6").select2();
});

$(function () {
	$("table.table tr").click(function () {
		window.location.href = $(this).data("url");
	});
});
