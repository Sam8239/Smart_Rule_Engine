// Loader Starts
const loader = document.getElementsByClassName("loader-div")
window.addEventListener("load", () => {
	loader[0].style.display = "none"
})
// Loader Ends

$(document).ready(function () {
	// Select2 Starts
	$(".js-example-basic-single").select2();
	$("#cname-modal").select2({
		dropdownParent: $("#exampleModal")
	});
	$("#cname").select2();
	$("#select1").select2();
	$("#select2").select2();
	$("#select3").select2();
	$("#select4").select2();
	$("#select5").select2();
	$("#select6").select2();
	// Select2 Ends

	// Onclick Table Rows Starts
	$(".tclick tr").click(function () {
		window.location.href = $(this).data("url");
	});
	// Onclick Table Rows Ends

	// Table Search Starts
	$("#myInput").on("keyup", function () {
		var value = $(this).val().toLowerCase();
		$("tbody tr").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});
	});
	// Table Search Ends
});

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

// Confirm Deletion Starts
document.addEventListener("DOMContentLoaded", function () {
	var deleteForm = document.getElementById("deleteForm");
	var confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

	if (confirmDeleteBtn) {
		// Set the parameter ID when the modal is shown
		$('#confirmDeleteModal').on('show.bs.modal', function (event) {
			confirmDeleteBtn.dataset.parameterId = $(event.relatedTarget).data('parameter-id');
		});

		// Handle the confirmation and form submission
		confirmDeleteBtn.addEventListener("click", function () {
			var parameterId = this.dataset.parameterId;
			// Set the form action with the correct parameter ID
			deleteForm.action = "parameters/del_parameter/" + parameterId + "/";
			deleteForm.submit();
		});
	}

});

// Confirm Deletion Ends



