$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


$(document).ready(function(){
    /*$('.search_friends').click(function(){
        $.post("/search_friends", {search_friends:$('input[name=search_friends]').val()})
        return false;

    })*/

    $('.add_friends').click(function(){
        var profilename = $(this).closest('td').find('input[name=username]').val();
        var parenttd = $(this).closest('td')
        $.post('/add_friends', {'profile_name':profilename},
            function(data) {
                if(data == "success"){
                    parenttd.find('.delete_friends').show();
                    parenttd.find('.add_friends').hide();
                }
                else{
                    alert(data);
                }
            });
        return false;

    });

    $('.delete_friends').click(function(){
        var profilename = $(this).closest('td').find('input[name=username]').val();
        var parenttd = $(this).closest('td')
        $.post("/delete_friends", {'profile_name':profilename, rnd: Math.random()},
            function(data) {
                if(data == "success"){
                    parenttd.find('.add_friends').show();
                    parenttd.find('.delete_friends').hide();
                }
                else{
                    alert(data);
                }
            });
        return false;

    });
})
