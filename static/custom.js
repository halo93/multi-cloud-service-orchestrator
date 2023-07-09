$(function() {
    // Takes a URL, param name, and data string
    jQuery.download = function(url, key, data, callback) {
        // Build a form
        let form = $('<form></form>').attr('action', url).attr('method', 'post');
        // Add the one key/value
        form.append($("<input></input>").attr('type', 'hidden').attr('name', key).attr('value', data));
        form.on("submit", function (e) {
            callback();
        })
        //send request
        form.appendTo('body').submit().remove();
    };

});