const data = document.currentScript.dataset
const csrf = data.csrf

const getData = () => ({
  materiais: [],
  cliente: {},
  clienteSelecionado: {},
  searchMaterial: '',
  servicos: [],
  itens: [],
  rdos: [],
  bms: [],
  servico: {},
  servicoSelecionado: {},
  searchServico: '',
  searchItem: '',
  searchUnidade: '',
  searchSolicitante: '',
  searchProjeto: '',
  searchEscopo: '',
  searchBms: '',
  ordemServico: {},
  ordemServicoItem: {},
  currentId: 1,
  ordemServicoItems: [],
  materiaisShow: false,
  servicosShow: false,
  rdosShow: false,
  bmsShow: false,

  init() {
    // watch - monitora as ações
    this.$watch('searchMaterial', (newValue, oldValue) => {
      if (!newValue) this.materiais = []
      if (newValue.length >= 1) {
        this.getClientes(newValue)
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
    this.$watch('searchUnidade', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 2) {
        this.getRdo_unidade(newValue)
      }
    })
    this.$watch('searchSolicitante', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 3) {
        this.getRdo_solicitante(newValue)
      }
    })
    this.$watch('searchProjeto', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 3) {
        this.getRdo_projeto(newValue)
      }
    })
    this.$watch('searchEscopo', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 3) {
        this.getRdo_escopo(newValue)
      }
    })
    this.$watch('searchBms', (newValue, oldValue) => {
      if (!newValue) this.itens = []
      if (newValue.length >= 5) {
        this.getBm_list(newValue)
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

  getClientes(newValue) {
    const search = newValue
    fetch(`/api/v1/material/material/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.materiais = data
        this.materiaisShow = true
      })
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

  getRdo_solicitante(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/rdo-solicitante/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.rdos = data
        this.rdosShow = true
      })
  },
  getRdo_unidade(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/rdo-unidade/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.rdos = data
        this.rdosShow = true
      })
  },
  getRdo_projeto(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/rdo-projeto/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.rdos = data
        this.rdosShow = true
      })
  },
  getRdo_escopo(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/rdo-escopo/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.rdos = data
        this.rdosShow = true
      })
  },
  getBm_list(newValue) {
    const search = newValue
    fetch(`/api/v1/rdo/boletimmedicao/?search=${search}`)
      .then(response => response.json())
      .then(data => {
        this.bms = data
        this.bmsShow = true
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