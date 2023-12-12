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
    document.getElementById("id_qtdand").max = item.qtd;

    // Adiciona a lógica para habilitar ou desabilitar a validação com base no valor de "id_montagem"
    if (document.getElementById("id_montagem").value === "DESMONTAGEM") {
      document.getElementById("id_qtdand").addEventListener("input", validarQuantidade);
    } else {
      document.getElementById("id_qtdand").removeEventListener("input", validarQuantidade);

  }},
 
  

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