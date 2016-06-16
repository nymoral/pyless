function remove_error(element) {
    var grandParent = element.parentNode.parentNode;
    $(grandParent).removeClass('has-error');
}

var guess_re = /^.*(\d+).*([-_:;., ]).*(\d+).*$/;
var input_name_re = /^game_input_(\d+)$/;

function guess_changed(element) {
    var val = element.value;
    var m = guess_re.exec(val);
    if (m && m.length == 4) {
        element.value = m[1] + ' : ' + m[3];
		update_single(element, m[1], m[3]);
    }
}

function make_put_url(game_id, g1, g2) {
	return './' + game_id + '/' + g1 + '/' + g2 + '/';
}

function update_single(input, g1, g2) {
	var m = input_name_re.exec(input.name);
	if (m && m.length == 2) {
		var game_id = m[1];
		$.ajax({
			url: make_put_url(game_id, g1, g2),
			method: 'PUT',
			success: function(response) {
				flash_success(input);
			},
			error: function(response) {
				console.log('ERROR');
				console.log(response);
			}
		});
	}
}

function flash_success(input) {
	var $el = $(input);
	$el.fadeTo(500, 0.5).promise().done(function() {
		$el.fadeTo(500, 1.0);
	});
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var cookie = getCookie('csrftoken');
$.ajaxSetup({ 
	beforeSend: function(xhr, settings) {
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			xhr.setRequestHeader("X-CSRFToken", cookie);
		}
	} 
});
