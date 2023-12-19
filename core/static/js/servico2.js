const data = document.currentScript.dataset
const csrf = data.csrf

const getData = () => ({
  placas: [],
  cliente: {},
  clienteSelecionado: {},
  searchMaterial: '',
  servicos: [],
  itens: [],
  rdos: [],
  bms: [],
  servico: {},
  servicoSelecionado: {},
  placaSelecionada: {'qtd':'m'},
  item: {},
  searchServico: '',
  searchItem: '',
  searchUnidade: '',
  searchSolicitante: '',
  searchProjeto: '',
  searchEscopo: '',
  searchPlaca: '',
  ordemServico: {},
  ordemServicoItem: {},
  currentId: 1,
  ordemServicoItems: [],
  materiaisShow: false,
  servicosShow: false,
  placasShow: false,
  rdosShow: false,
  bmsShow: false,

  init() {
    
    // watch - monitora as ações
    this.$watch('searchPlaca', (newValue, oldValue) => {
      if (!newValue) this.placas = []
      if (newValue.length >= 3) {
        this.getPlacas(newValue)
      }
    })
    this.$watch('searchServico', (newValue, oldValue) => {
      if (!newValue) this.servicos = []
      if (newValue.length >= 3) {
        this.getServicos(newValue)
      }
    })
    this.$watch('searchItem', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 5) {
        this.getItens(newValue)
      }
    })
  },

  addItem() {
    
    // Envia os dados para inserir um novo item na Ordem de Serviço Item,
    // que por sua vez será retornado na tabela de itens.
    const servico_id = this.servicoSelecionado.id
    const servico_titulo = this.servicoSelecionado.titulo
    const valor = this.ordemServicoItem.valor
    const proxima_visita = this.ordemServicoItem.proximaVisita

    let ordem_servico_item_id = this.currentId++
    this.ordemServicoItems.push({ id: ordem_servico_item_id, servico_id, servico_titulo, valor, proxima_visita })
  },

  deleteOrdemServicoItem(id) {
    const indexToRemove = this.ordemServicoItems.findIndex(i => i.id == id)
    this.ordemServicoItems.splice(indexToRemove, 1)
  },
 
  getPlacas(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/placa/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.placas = data
        this.placasShow = true
      })
  },
  getPlaca(item) {
    this.placaSelecionada = item
    this.placasShow = false

    document.getElementById("id_placa").value = item.placa;

    document.getElementById("id_qtdandtub").removeEventListener("input", function () {
        validarQuantidade("id_qtdandtub", item.qtd_t);
    });
    document.getElementById("id_qtdandtub").max = item.qtd_t;

    // Adiciona a lógica para habilitar ou desabilitar a validação com base no valor de "id_montagem"
    if (document.getElementById("id_montagem").value === "DESMONTAGEM") {
      document.getElementById("id_qtdandtub").addEventListener("input", function () {
          validarQuantidade("id_qtdandtub", item.qtd_t);
      });
  } else {
      document.getElementById("id_qtdandtub").removeEventListener("input", function () {
          validarQuantidade("id_qtdandtub", item.qtd_t);
      });
  }

    document.getElementById("id_qtdandenc").max = item.qtd_e;

    if (document.getElementById("id_montagem").value === "DESMONTAGEM") {
      document.getElementById("id_qtdandenc").addEventListener("input", function () {
          validarQuantidade("id_qtdandenc", item.qtd_e);
      });
  } else {
      document.getElementById("id_qtdandenc").removeEventListener("input", function () {
          validarQuantidade("id_qtdandenc", item.qtd_e);
      });
  }

  document.getElementById("id_qtdpra").max = item.qtd_pranchao;
    
  if (document.getElementById("id_montagem").value === "DESMONTAGEM") {
    document.getElementById("id_qtdpra").addEventListener("input", function () {
        validarQuantidade("id_qtdpra", item.qtd_pranchao);
    });
} else {
    document.getElementById("id_qtdpra").removeEventListener("input", function () {
        validarQuantidade("id_qtdpra", item.qtd_pranchao);
    });
}
document.getElementById("id_qtdpis").max = item.qtd_piso;
    
  if (document.getElementById("id_montagem").value === "DESMONTAGEM") {
    document.getElementById("id_qtdpis").addEventListener("input", function () {
        validarQuantidade("id_qtdpis", item.qtd_piso);
    });
} else {
    document.getElementById("id_qtdpis").removeEventListener("input", function () {
        validarQuantidade("id_qtdpis", item.qtd_piso);
    });
}
},
 
  

  getCliente(cliente) {
    this.clienteSelecionado = cliente
    this.clienteShow = false
  },

  getServicos(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/itembm/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.servicos = data
        this.servicosShow = true
      })
  },
  getItens(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/itembm-item/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.servicos = data
        this.servicosShow = true
      })
  },


  getServico(servico) {
    this.servicoSelecionado = servico
    this.servicosShow = false
  },

  saveData() {
    const cliente_id = this.clienteSelecionado.id
    const situacao = this.ordemServico.situacao
    const ordem_servico_itens = this.ordemServicoItems
    const bodyData = { cliente_id, situacao, ordem_servico_itens }
    fetch('/api/v1/servico/ordem-servico/', {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify(bodyData),
      })
      .then(response => response.json())
      .then(data => {
        // redirect para os detalhes da OrdemServico
        const ordem_servico_id = data.ordem_servico_id
        window.location.href = `/servico/${ordem_servico_id}/`
      })
  },
  

})

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
    let self = $(this)
    mat_val = $("#materialCalculo").val()
    $.ajax({
        url:url,
        type: 'GET',
        success: function(response){
            fator = response.data[mat_val][chave]
            $('#polfator').val(fator)
        },
        error: function(xhr){
            //body
        }
    })
});
$(document).on('change', '.clQTD', function(){ 
    quantidade = $(this).val()
    resultado = quantidade * $('#polfator').val()
    resultado_2 = resultado.toFixed(3)
    $('#resultadoCalculo').val(resultado_2)
    $('#resultadoCalculo').text(resultado_2)

});


$(document).on('change', '.clLados', function(){ 
    let lado = $(this).val()
    let comprimento = $("#comprimentoCalculo").val()
    let largura = $("#larguraCalculo").val()
    let altura = $("#alturaCalculo").val()
    let raio = $("#raioCalculo").val()
    let material = $("#materialCalculo").val()
    const PI = 3.14156;
    let geratriz = Math.sqrt(raio**2+altura**2)
    let retorno
    

    if (material == "boleado") {
        retorno = (PI* (raio ** 2/4 + altura ** 2)) * lado;
        $('#resultadoCalculo').val(retorno.toFixed(3))
        $('#resultadoCalculo').text(retorno.toFixed(3))
    } else if (material == "carretel") {
        retorno = 2*raio*PI*altura*lado;
        $('#resultadoCalculo').val(retorno.toFixed(3))      
        $('#resultadoCalculo').text(retorno.toFixed(3))
    } else if (material == "cubo") {
        retorno = (largura*altura*2+largura*comprimento*2+altura*comprimento*2)*lado;
        $('#resultadoCalculo').val(retorno.toFixed(3))
        $('#resultadoCalculo').text(retorno.toFixed(3))
    } else if (material == "cone") {
        retorno = PI*raio**2+PI*raio*geratriz; 
       $('#resultadoCalculo').val(retorno.toFixed(3)) 
       $('#resultadoCalculo').text(retorno.toFixed(3))
    } else if (material == "janela") {
        retorno = largura*altura*lado*comprimento;
        $('#resultadoCalculo').val(retorno.toFixed(3))
        $('#resultadoCalculo').text(retorno.toFixed(3))
    } else {
        retorno = 0.00;
        $('#resultadoCalculo').text(retorno.toFixed(3))
    }
});