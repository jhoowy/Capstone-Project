function keyWordsearch() {
    $(".loader").show();
    gapi.client.setApiKey("AIzaSyBUwoEoNLZJEOf20a5ccpLCbysdlzHl0bQ");
    gapi.client.load('youtube', 'v3', function() {
        makeRequest();
    });
}

function makeRequest(page) {
    var q = $('#query').val();
    var request = gapi.client.youtube.search.list({
        q: q,
        part: 'snippet',
        maxResults: 10,
        pageToken: page
    });

    request.execute(function(response) {
        var nextpage = response.nextPageToken;
        var prevpage = response.prevPageToken;

        $("#prev").click(function() {
            $(".loader").show();
            makeRequest(prevpage);
            $("body").scrollTop(0);
            $(".loader").fadeOut("slow");
        });
        $("#next").click(function() {
            $(".loader").show();
            makeRequest(nextpage);
            $("body").scrollTop(0);
            $(".loader").fadeOut("slow");
        });

        $('#results').empty();
        var srchItems = response.result.items;

        $.each(srchItems, function(index, item) {
            vidTitle = item.snippet.title;
            vidId = item.id.videoId;
            vidDescription = item.snippet.description;
            console.log(response);

            let url = "'https://youtu.be/" + vidId + "'";

            // ToDo: a href="/search/download/{{vid}} 부분 구현하기
            $('#list').append('<div class="videoItem" style="text-align: left;">\
                <a href="#" onclick="uploadUrl(' + url + ');" class="title">' + vidTitle + '</a>\
                <p class="author">' + 'Description:  <br/>' + vidDescription.substr(0, 135) + '...</p>\
                <div class="embed-responsive embed-responsive-16by9">\
                    <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/' + vidId + '"</iframe>\
                </div>\
            </div>');
            $(".nextpr").css('display', 'inline');
            $('.title').click(function() {
                 setTimeout(function() {   
                    $(".loader").fadeOut("slow");
                }, 1000);
            });
        })
    });
}

function uploadUrl(url) {
    var formdata = new FormData();
    formdata.append('url', url);
    $.ajax({
        url: 'upload_url',
        type: 'post',
        processData: false,
        contentType: false,
        data: formdata,
        success: function(data) {
            window.location.href = '/process/' + data;
            console.log(data)
        },
        error: function(data){
            alert(data);
        }
    })
}
