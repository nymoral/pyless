function remove_error(element) {
    var grandParent = element.parentNode.parentNode;
    $(grandParent).removeClass('has-error');
}

var guess_re = /^.*(\d+).*([-_:;., ]).*(\d+).*$/;
function guess_changed(element) {
    var val = element.value;
    var m = guess_re.exec(val);
    if (m && m.length == 4) {
        element.value = m[1] + ' : ' + m[3];
    }
}