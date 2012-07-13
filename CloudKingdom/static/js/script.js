function change_img(button) {
	var e = $(button).parent().parent();
	var id = e.find("#img_id");
	var name = e.find("#img_name");
	var driver = e.find("#img_driver");

	var finish = $("#finish_img");
	finish.find("#img_id").html(id.html());
	finish.find("#img_name").html(name.html());
	finish.find("#img_driver").html(driver.html());
}

function change_size(button) {
	var e = $(button).parent().parent();
	var id = e.find("#size_id");
	var name = e.find("#size_name");
	var disk = e.find("#size_disk");
	var uuid = e.find("#size_uuid");
	var ram = e.find("#size_ram");

	var finish = $("#finish_size");
	finish.find("#size_id").html(id.html());
	finish.find("#size_name").html(name.html());
	finish.find("#size_uuid").html(uuid.html());
	finish.find("#size_ram").html(ram.html());
	finish.find("#size_disk").html(disk.html());
}

function delete_node(obj) {
	var e = $(obj).parent().parent();
	var id = e.find("#img_id").text();
	var name = e.find("#img_name").text();
	var uuid = e.find("#img_uuid").text();
	$.post('/delete/', {"id": id, "name": name, "uuid": uuid}, function(data) {
		console.log(data);
	});
	return false;
}

$(document).ready(function() {

	$(".initial-expand").hide();

	$("div.content-module-heading").click(function(){
		$(this).next("div.content-module-main").slideToggle();

		$(this).children(".expand-collapse-text").toggle();
	});

	console.log($("#zInput"));
	$("#zInput").change(function() {
		var instance_name = $(this).val();
		$("#instance-name").text(instance_name);
	});

	$("#submit_request").click(function() {
		var image = $("#finish_img").find("#img_id").text();
		var size = $("#finish_size").find("#size_id").text();
		var name = $("#zInput").val();

		$.post('./createinstance/', {"image": image, "size": size, "name": name}, function(data) {
			console.log(data);
		});
		return false;
	});

	$(".delete").click(function() {

		var e = $(this).parent().parent();
		var id = e.find("#img_id").text();
		var name = e.find("#img_name").text();
		var uuid = e.find("#img_uuid").text();

		$.post('/delete/', {"id": id, "name": name, "uuid": uuid}, function(data) {
			console.log(data);
		});

		return false;
	});

});
