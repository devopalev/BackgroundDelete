$(document).ready(function(){

	var dropZone = $('#upload-container');

	$('#file-input').focus(function() {
		$('label').addClass('focus');
	})
	.focusout(function() {
		$('label').removeClass('focus');
	});


	dropZone.on('drag dragstart dragend dragover dragenter dragleave drop', function(){
		return false;
	});

	dropZone.on('dragover dragenter', function() {
		dropZone.addClass('dragover');
	});

	dropZone.on('dragleave', function(e) {
		let dx = e.pageX - dropZone.offset().left;
		let dy = e.pageY - dropZone.offset().top;
		if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
			dropZone.removeClass('dragover');
		}
	});

	dropZone.on('drop', function(e) {
		dropZone.removeClass('dragover');
		let files = e.originalEvent.dataTransfer.files;
		preSendFiles();
		sendFiles(files);
	});

	$('#file-input').change(function() {
		let files = this.files;
		preSendFiles();
		sendFiles(files);
	});


	function preSendFiles() {
		$('#upload-header').html('Обрабатываю фото. Подожди немного.');
		$('#upload-container').css('display', 'none');
		$('.loader').css('display', 'block');
	}

	function postSendfiles() {
		$('#upload-header').html('Готово! Загрузка начнется автоматически.<br>Обработаем ещё фото?');
		$('.loader').css('display', 'none');
		$('#upload-container').css('display', 'flex');
	}


	function sendFiles(files) {
		let maxFileSize = 5242880;
		let Data = new FormData();
		$(files).each(function(index, file) {
			if ((file.size <= maxFileSize) && ((file.type == 'image/png') || (file.type == 'image/jpeg') || (file.type == 'image/jpg'))) {
				Data.append('images[]', file);
			};
		});
		$.ajax({
			url: dropZone.attr('action'),
			type: dropZone.attr('method'),
			data: Data,
			dataType: 'binary',
			xhrFields: {
				'responseType': 'blob'
			},
			contentType: false,
			processData: false,
			success: function(data, status, xhr) {
				var fileName = xhr.getResponseHeader('content-disposition').split('filename=')[1];
				var blob = new Blob([data], {type: xhr.getResponseHeader('Content-Type')});
				var link = document.createElement('a');
				link.href = window.URL.createObjectURL(blob);
				link.download = fileName;
				link.click();
				postSendfiles();
			},
			error: function (jqXHR, exception) {
				if (jqXHR.status === 0) {
					alert('Кажется пропал интернет.. Либо у тебя, либо у меня :(');
				} else if (jqXHR.status == 404) {
					alert('Requested page not found (404).');
				} else if (jqXHR.status == 500) {
					alert('Упс! Что-то пошло не так :( Попробуй ещё раз.');
				} else if (exception === 'parsererror') {
					alert('Упс! Что-то пошло не так :(');
				} else if (exception === 'timeout') {
					alert('Упс! Что-то пошло не так :( Попробуй ещё раз.');
				} else if (exception === 'abort') {
					alert('Упс! Что-то пошло не так :(');
				} else {
					alert('Uncaught Error. ' + jqXHR.responseText);
				}
				location.reload();
			}
		});
	}
})