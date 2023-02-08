
$(document).ready(function(){
    $('#id_romaneio-0-material').addClass('clMaterial')
    $('#id_romaneio-0-m_quantidade').addClass('clQuantidade')
    $('#id_romaneio-0-polegada').addClass('clPolegada')
    //esconde o m2
    $('#id_romaneio-0-m2').prop('type', 'hidden')
    $('label[for="id_romaneio-0-m2"]').append('<span id="id_romaneio-0-m2-span" class="lead" style="padding: 10px 40px;font-weight: bolder;"></span>')

    $('#add-item').click(function(ev){
        ev.preventDefault();
        var count = $('#romaneio').children().length;
        var tmplMarkup = $('#item-romaneio').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#romaneio').append(compiledTmpl);

        //update form-count
        $('#id_romaneio-TOTAL_FORMS').attr('value', count + 1);
        // esconde o m2
        $('#id_romaneio-' + (count) + '-m2').prop('type', 'hidden')
        // some animatescroll to view form
        $('html, body').animate({
            scrollTop: $("#add-item").position().top - 200
        }, 800);

        $('#id_romaneio-' + (count) + '-material').addClass('clMaterial')
        $('#id_romaneio-' + (count) + '-m_quantidade').addClass('clQuantidade')
        $('#id_romaneio-' + (count) + '-polegada').addClass('clPolegada')
        // cria span para mostrar saldo na tela
        $('label[for="id_romaneio-' + (count) + '-m2"]').append('<span id="id_romaneio-' + (count) + '-m2-span" class="lead" style="padding: 10px 40px;font-weight: bolder;"></span>')

    });
});

let quantidade
let campo
let fator
let resultado
let resultado_2
let mat
let mat_val
let campo2

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
    resultado_2 = resultado.toFixed(3)
    $('#'+campo).prop('type', 'hidden')
    $('#'+campo).val(resultado_2)
    campo2 = $(this).attr('id').replace('m_quantidade', 'm2-span')
    $('#'+campo2).text(resultado_2)

});
