var zip = $('[data-cepbrinput=zip]');
var street = $('[data-cepbrinput=street]');
var city = $('[data-cepbrinput=city]');
var larea = $('[data-cepbrinput=larea]');
var state = $('[data-cepbrinput=state]');

function updateFields(){
    value = zip.val();
    if ((value)){
        $.ajax({
            method: "GET",
            url: zip.data('url'),
            data: {'zip': value},
            success: function(data){
                street.val(data.logradouro);
                larea.val(data.bairro);
                city.val(data.localidade);
                state.val(data.uf);
            },
        });
    }
}


$(function (){
    updateFields();
    zip.blur(updateFields);
});