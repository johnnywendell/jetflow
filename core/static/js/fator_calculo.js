
$(document).ready(function(){
    $('#id_romaneio-0-material').addClass('clMaterial')
    $('#id_romaneio-0-m_quantidade').addClass('clQuantidade')
    $('#id_romaneio-0-polegada').addClass('clPolegada')

    $('#add-item').click(function(ev){
        ev.preventDefault();
        var count = $('#romaneio').children().length;
        var tmplMarkup = $('#item-romaneio').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#romaneio').append(compiledTmpl);

        //update form-count
        $('#id_romaneio-TOTAL_FORMS').attr('value', count + 1);
        // some animatescroll to view form
        $('html, body').animate({
            scrollTop: $("#add-item").position().top - 200
        }, 800);

        $('#id_romaneio-' + (count) + '-material').addClass('clMaterial')
        $('#id_romaneio-' + (count) + '-m_quantidade').addClass('clQuantidade')
        $('#id_romaneio-' + (count) + '-polegada').addClass('clPolegada')
    });
});

let quantidade
let campo
let fator
let resultado
let mat
let mat_val

$(document).on('change', '.clPolegada', function(){
    let url = '/romaneios/json'
    let chave = $(this).val()
    mat = $(this).attr('id').replace('polegada','material')
    mat_val = $('#'+mat).val()
    $.ajax({
        url:url,
        type: 'GET',
        success: function(response){
            fator = response.data[mat_val][chave]
        },
        error: function(xhr){
            //body
        }
    })
});
$(document).on('change', '.clQuantidade', function(){ 
    quantidade = $(this).val()
    campo = $(this).attr('id').replace('m_quantidade','m2')
    resultado = quantidade * fator
    $('#'+campo).val(resultado)
});
