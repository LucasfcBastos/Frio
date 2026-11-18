/** Portuguese (default). Every UI string lives here; `en.ts` must mirror this shape. */
export const ptBR = {
  app: { name: 'FrioGuard', tagline: 'Segurança para refrigeração conectada' },
  nav: {
    label: 'Navegação principal',
    dashboard: 'Painel',
    equipment: 'Equipamentos',
    incidents: 'Incidentes',
    vulnerabilities: 'Vulnerabilidades',
    settings: 'Configurações',
    comingSoon: 'Em breve',
    openMenu: 'Abrir menu',
    closeMenu: 'Fechar menu',
  },
  header: {
    store: 'Loja',
    storeLoading: 'Carregando lojas…',
    language: 'Idioma',
    updatedAgo: 'Atualizado {time}',
    waitingData: 'Aguardando dados',
    live: 'Ao vivo',
    user: { name: 'Ana Souza', role: 'Analista de segurança' },
    overall: {
      normal: 'Todos os sistemas normais',
      warning: 'Atenção necessária',
      critical: 'Incidente crítico em andamento',
    },
  },
  dashboard: {
    title: 'Painel de Monitoramento',
    subtitle: '{store} · {city}/{state}',
    equipmentSection: 'Equipamentos',
    equipmentHint: 'Selecione um equipamento para ver o histórico',
    chartSection: 'Temperatura · últimas {hours}h',
    incidentSection: 'Incidentes ativos',
  },
  kpi: {
    monitored: 'Equipamentos monitorados',
    monitoredHint: 'Controladores + sensores independentes',
    normal: 'Em operação normal',
    normalHint: 'Atenção: {warning} · Críticos: {critical}',
    activeAlerts: 'Alertas ativos',
    activeAlertsHint: 'Incidentes abertos nesta loja',
    noAlertsHint: 'Nenhum incidente aberto',
    detectionTime: 'Tempo médio de detecção',
    detectionTimeHint: 'vs. 3h30 no ataque da Suécia',
    firmware: 'Firmware vulnerável',
    firmwareHint: 'de {total} controladores desatualizados',
    noData: '—',
  },
  banner: {
    label: 'Incidente crítico',
    meta: '{equipment} · iniciado {time}',
    details: 'Ver detalhes',
  },
  equipment: {
    type: { freezer: 'Freezer', cold_room: 'Câmara fria', chiller: 'Resfriado' },
    mode: { cooling: 'Resfriando', defrost: 'Degelo', idle: 'Em espera' },
    controller: 'Controlador',
    sensor: 'Sensor independente',
    setpoint: 'Setpoint',
    modeLabel: 'Modo',
    diverging: 'Divergência de {value}',
    firmwareOutdated: 'Firmware {version} desatualizado',
    selected: 'Selecionado',
    sparklineLabel: 'Tendência do sensor independente',
    empty: 'Nenhum equipamento cadastrado nesta loja.',
  },
  status: { normal: 'Normal', warning: 'Atenção', critical: 'Crítico' },
  severity: { low: 'Baixa', medium: 'Média', high: 'Alta', critical: 'Crítica' },
  chart: {
    controller: 'Controlador',
    sensor: 'Sensor independente',
    setpoint: 'Setpoint',
    safeRange: 'Faixa segura',
    incidentStart: 'Início do incidente',
    empty: 'Sem leituras no período.',
    noSelection: 'Selecione um equipamento.',
    ariaLabel: 'Gráfico de temperatura de {name}',
  },
  incidents: {
    empty: 'Nenhum incidente ativo. Tudo sob controle.',
    rule: 'Regra',
    detectedIn: 'detectado em {time}',
  },
  rules: {
    UNSCHEDULED_DEFROST: {
      title: 'Degelo fora da janela programada',
      description:
        '{equipment} entrou em degelo às {started_local}, fora das janelas programadas ({schedule}). O compressor está desligado enquanto o controlador continua reportando temperatura normal.',
    },
    SENSOR_DIVERGENCE: {
      title: 'Controlador e sensor independente divergem',
      description:
        'O controlador reporta {controller_c}°C enquanto o sensor independente mede {sensor_c}°C ({divergence_c}°C de diferença; limite {threshold_c}°C). A telemetria do controlador pode estar falsificada.',
    },
    OUT_OF_SAFE_RANGE: {
      title: 'Temperatura fora da faixa segura',
      description:
        'Leitura de {temperature_c}°C; a faixa segura de {equipment} é de {safe_min_c}°C a {safe_max_c}°C.',
    },
    SETPOINT_TAMPERING: {
      title: 'Setpoint adulterado',
      description:
        'O setpoint de {equipment} foi alterado de {old_value}°C para {new_value}°C a partir do IP {origin_ip}.',
    },
  },
  drawer: {
    close: 'Fechar painel',
    description: 'Descrição',
    timeline: 'Linha do tempo',
    detectionTime: 'Tempo de detecção',
    origin: 'Origem',
    startedAt: 'Início',
    detectedAt: 'Detectado',
    timelineKinds: {
      config_change: 'Configuração alterada',
      condition_started: 'Condição iniciada',
      incident_detected: 'Incidente detectado',
    },
    configChange: '{field}: {old} → {new}',
    fromIp: 'IP de origem {ip}',
    detectedAfter: '{title} · em {time}',
    fields: {
      remote_access: 'Acesso remoto',
      high_temp_alarm_c: 'Alarme de alta temperatura (°C)',
      setpoint_c: 'Setpoint (°C)',
      defrost_mode: 'Modo de degelo',
    },
  },
  states: {
    error: 'Não foi possível carregar os dados.',
    retry: 'Tentar novamente',
    loading: 'Carregando…',
  },
  notFound: {
    title: 'Página não encontrada',
    description: 'O endereço acessado não existe.',
    back: 'Voltar ao painel',
  },
};

export type Messages = typeof ptBR;
