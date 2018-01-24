

$(document).ready(function(){
// the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $(".dropdown-button").dropdown(
        {
           inDuration: 300,
           outDuration: 225,
           constrain_width: true,
           hover: true,
           gutter: 0,
           belowOrigin: false
           }
    );
    $('.modal').modal();
});