function validateUrl(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
    var match = url.match(regExp);
    if (match && match[2].length == 11) {
        return true;
    }
    else {
        alert("Link is not valid!");
        return false;
    }
}

$('#upload').click(function() {
    var myfile = $('#btn_file')[0].files[0];
    var url = $('#url').val();
    var formdata = new FormData();

    var proc_btn = $('.process_btn');
    var loading = $('.loading-container');

    proc_btn.prop('disabled', true);
    proc_btn.addClass('hidden');
    loading.removeClass('hidden');
    
    if (myfile != null) {
        formdata.append('name', filename);
        formdata.append('file', myfile)
        $.ajax({
            url: 'upload',
            type: 'post',
            processData: false,
            contentType: false,
            data: formdata,
            success: function(data) {
                var href = window.location.href.trim().split('/')
                href = href.join('/') + "process/" + data

                window.location.href = href;
                console.log(data)
            },
            error: function(data){
                proc_btn.prop('disabled', false);
                loading.addClass('hidden');
                proc_btn.removeClass('hidden');
                alert(data);
            }
        })
    }
    else if (url != undefined && url != '') {
        if (validateUrl(url)) {
            formdata.append('url', url);
            $.ajax({
                url: 'upload_url',
                type: 'post',
                processData: false,
                contentType: false,
                data: formdata,
                success: function(data) {
                    var href = window.location.href.trim().split('/')
                    href = href.join('/') + "process/" + data
    
                    window.location.href = href;
                    console.log(data)
                },
                error: function(data){
                    proc_btn.prop('disabled', false);
                    loading.addClass('hidden');
                    proc_btn.removeClass('hidden');
                    alert(data);
                }
            })
        }
    }
    else {
        proc_btn.prop('disabled', false);
        loading.addClass('hidden');
        proc_btn.removeClass('hidden');
        alert("Upload Video Please!");
    }
});