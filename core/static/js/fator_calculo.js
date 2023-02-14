
$(document).ready(function(){
    $('#id_romaneio-0-material').addClass('clMaterial')
    $('#id_romaneio-0-m_quantidade').addClass('clQuantidade')
    $('#id_romaneio-0-polegada').addClass('clPolegada')
    $('#id_romaneio-0-lados').addClass('clLados')
    //esconde o m2
    $('#id_romaneio-0-m2').prop('type', 'hidden')
    $('label[for="id_romaneio-0-m2"]').append('<span id="id_romaneio-0-m2-span" class="lead" style="width: 100px;font-weight: bolder;background-color: yellow;"></span>')

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
        $('#id_romaneio-' + (count) + '-lados').addClass('clLados')
        // cria span para mostrar saldo na tela
        $('label[for="id_romaneio-' + (count) + '-m2"]').append('<span id="id_romaneio-' + (count) + '-m2-span" class="lead" style="width: 100px;font-weight: bolder;background-color: yellow;"></span>')

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




$(document).on('change', '.clLados', function(){ 
    let lado = $(this).val()
    let comprimento = $('#'+($(this).attr('id').replace('lados','comprimento'))).val()
    let largura = $('#'+($(this).attr('id').replace('lados','largura'))).val()
    let altura = $('#'+($(this).attr('id').replace('lados','altura'))).val()
    let raio = $('#'+($(this).attr('id').replace('lados','raio'))).val()
    let material = $('#'+($(this).attr('id').replace('lados','material'))).val()
    const PI = 3.14156;
    let geratriz = Math.sqrt(raio**2+altura**2)
    let retorno
    

    if (material == "boleado") {
        retorno = (PI* (raio ** 2/4 + altura ** 2)) * lado;
        campo = $(this).attr('id').replace('lados','m2')
        $('#'+campo).val(retorno.toFixed(3))
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    } else if (material == "carretel") {
        retorno = 2*raio*PI*altura*lado;
        campo = $(this).attr('id').replace('lados','m2')
        $('#'+campo).val(retorno.toFixed(3))
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    } else if (material == "cubo") {
        retorno = (largura*altura*2+largura*comprimento*2+altura*comprimento*2)*lado;
        campo = $(this).attr('id').replace('lados','m2')
        $('#'+campo).val(retorno.toFixed(3))
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    } else if (material == "cone") {
        retorno = PI*raio**2+PI*raio*geratriz;
        campo = $(this).attr('id').replace('lados','m2')
        $('#'+campo).val(retorno.toFixed(3))
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    } else if (material == "janela") {
        retorno = largura*altura*lado*comprimento;
        campo = $(this).attr('id').replace('lados','m2')
        $('#'+campo).val(retorno.toFixed(3))
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    } else {
        retorno = 0.00;
        campo2 = $(this).attr('id').replace('lados', 'm2-span')
        $('#'+campo2).text(retorno.toFixed(3))
    }
});

