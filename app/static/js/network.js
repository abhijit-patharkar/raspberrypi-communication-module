$(function(){
    var validateForm = function() {
        var address = $("input[name=nameGoesHere]").val();
        var netmask = $("input[name=netmask]").val();
        var gateway = $("input[name=gateway]").val();

        if(!address && !netmask && !gateway) {
            return false;
        }
        return true;
    }

    $('#saveBttn').click(function() {
        console.log('clicked');
        if(!validateForm()) {
            $('#err-div').addClass('show').removeClass('hide');
            return false;
        }

        $('#err-div').addClass('hide').removeClass('show');
        //$('#network_form').submit();
    });

    $('.title').click(function() {
        console.log('sdfsdf');
    });

});