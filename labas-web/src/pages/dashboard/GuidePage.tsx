import { useState } from "react";
import {
  Box,
  Tab,
  Tabs,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import CircleIcon from "@mui/icons-material/Circle";

interface TabPanelProps {
  children: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel({ children, index, value }: TabPanelProps) {
  return (
    <Box role="tabpanel" hidden={value !== index} sx={{ py: 3 }}>
      {value === index && children}
    </Box>
  );
}

interface SecaoProps {
  titulo: string;
  descricao: string;
  passos: string[];
  dicas?: string[];
}

function SecaoGuia({ titulo, descricao, passos, dicas }: SecaoProps) {
  return (
    <Box>
      <Typography variant="h6" fontWeight={700} gutterBottom>
        {titulo}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        {descricao}
      </Typography>

      <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1 }}>
        Passo a passo:
      </Typography>
      <List dense disablePadding sx={{ mb: 2 }}>
        {passos.map((passo, i) => (
          <ListItem key={i} disableGutters>
            <ListItemIcon sx={{ minWidth: 28 }}>
              <CircleIcon sx={{ fontSize: 8, color: "primary.main" }} />
            </ListItemIcon>
            <ListItemText
              primary={
                <Typography variant="body2">
                  <strong>{i + 1}.</strong> {passo}
                </Typography>
              }
            />
          </ListItem>
        ))}
      </List>

      {dicas && dicas.length > 0 && (
        <>
          <Typography variant="subtitle2" fontWeight={600} sx={{ mb: 1 }}>
            Dicas:
          </Typography>
          {dicas.map((dica, i) => (
            <Box
              key={i}
              sx={{
                bgcolor: "primary.main",
                borderRadius: 1,
                px: 2,
                py: 1,
                mb: 1,
              }}
            >
              <Typography
                variant="body2"
                fontWeight={700}
                sx={{ color: "white" }}
              >
                {dica}
              </Typography>
            </Box>
          ))}
        </>
      )}
    </Box>
  );
}

const abas = [
  "Visão Geral",
  "Calibração",
  "Entrada de Amostras",
  "Laudos",
  "Clientes",
];

const conteudo: SecaoProps[] = [
  {
    titulo: "Visão Geral do LABAS",
    descricao:
      "O LABAS é o sistema de gestão do laboratório de análise de solos e sementes. Centralize todo o fluxo desde o cadastro de clientes até a emissão do laudo final.",
    passos: [
      "Cadastre o cliente antes de qualquer coisa — sem cliente não é possível criar um laudo.",
      "Calibre o equipamento correto e verifique se a bateria está ativa para o elemento desejado.",
      "Crie o laudo e associe-o ao cliente cadastrado.",
      "Acesse 'Amostras' e insira as leituras brutas em lote para as análises desse laudo.",
      "Volte ao laudo e verifique quais amostras devem constar no PDF (ative/inative pelo toggle).",
      "Gere o PDF com todas as análises ativas e entregue ao cliente.",
    ],
    dicas: [
      "Fluxo correto: Cadastrar Cliente → Calibrar Equipamento (bateria ativa) → Criar Laudo → Inserir Amostras → Revisar Análises → Gerar PDF.",
      "Apenas técnicos (staff) têm acesso completo. Clientes visualizam apenas seus laudos e fazem download do PDF.",
      "Nunca insira amostras sem antes confirmar que a bateria está ativa para o elemento correspondente.",
    ],
  },
  {
    titulo: "Calibração de Equipamentos",
    descricao:
      "O módulo de calibração gerencia as baterias de calibração de cada equipamento (AA, FC, ES, pH). Uma bateria ativa é necessária para que os resultados das amostras sejam calculados corretamente.",
    passos: [
      "Acesse 'Calibração' na sidebar.",
      "Clique em 'Nova Calibração' e selecione o equipamento e elemento.",
      "Insira os pontos de calibração: concentração e leitura bruta do padrão.",
      "O sistema calculará automaticamente a curva y = ax + b e o R².",
      "Verifique que o R² está acima do mínimo aceitável e ative a bateria.",
      "Somente uma bateria por elemento/equipamento pode estar ativa por vez.",
    ],
    dicas: [
      "O branco deve ser inserido como ponto com concentração 0.",
      "Se o R² estiver baixo, revise as leituras dos padrões antes de ativar.",
    ],
  },
  {
    titulo: "Entrada de Amostras (Operação em Lote)",
    descricao:
      "A tela de entrada de amostras permite inserir leituras brutas do equipamento em lote para um conjunto de análises. O sistema usa a bateria ativa do dia para calcular o resultado automaticamente.",
    passos: [
      "Acesse 'Amostras' na sidebar.",
      "Selecione o elemento que será lido (ex: Ca, Mg, K).",
      "Confirme a curva de calibração ativa exibida na tela.",
      "Para cada amostra, informe o N_Lab, o Fator de Diluição e a Leitura Bruta.",
      "Pressione Enter para avançar para a próxima linha — a leitura é salva em background.",
      "O resultado calculado aparece automaticamente na coluna 'Resultado'.",
    ],
    dicas: [
      "O N_Lab segue o padrão AAAA/NNN (ex: 2026/001).",
      "Se uma leitura precisar ser corrigida, acesse o Laudo correspondente e use o ícone de correção na análise.",
      "Certifique-se de que há uma bateria ativa para o elemento antes de inserir leituras.",
    ],
  },
  {
    titulo: "Laudos",
    descricao:
      "O módulo de laudos gerencia os documentos entregues aos clientes. Cada laudo pode conter até 50 análises de solo individuais. O PDF final é gerado com todas as análises ativas.",
    passos: [
      "Acesse 'Meus Laudos' na sidebar para ver a lista de laudos.",
      "Clique em 'Novo Laudo' para criar um cabeçalho: selecione o cliente e a data de entrada.",
      "Após criar o laudo, você será redirecionado para a tela de edição.",
      "As análises são associadas ao laudo via 'Entrada de Amostras'.",
      "Na tela de edição, você pode corrigir fichas, ajustar granulometria e inativar análises.",
      "Quando o laudo estiver pronto, clique em 'Gerar PDF' para baixar o documento.",
    ],
    dicas: [
      "O código do laudo (ex: L-2026/1) é gerado automaticamente — não é editável.",
      "Análises inativas (toggle desligado) não aparecem no PDF.",
      "Use o ícone de correção (tubo de ensaio) para ajustar leituras brutas sem precisar refazer toda a entrada.",
    ],
  },
  {
    titulo: "Clientes",
    descricao:
      "O módulo de clientes mantém o cadastro de produtores e empresas que enviam amostras ao laboratório.",
    passos: [
      "Acesse 'Clientes' na sidebar.",
      "Clique em 'Novo Cliente' para cadastrar: nome, código, endereço e contato.",
      "O código do cliente é usado para associá-lo a laudos — defina um padrão consistente (ex: iniciais + número).",
      "Use a busca para localizar clientes rapidamente pelo nome ou código.",
      "Clique em editar para atualizar os dados cadastrais a qualquer momento.",
    ],
    dicas: [
      "O código do cliente não pode ser alterado após a criação.",
      "Clientes inativos podem ter laudos associados — remova com cautela.",
    ],
  },
];

export default function GuidePage() {
  const [aba, setAba] = useState(0);

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} color="primary" gutterBottom>
        Guia de Uso do LABAS
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Consulte este guia para entender o fluxo de cada módulo do sistema.
      </Typography>

      <Paper variant="outlined">
        <Tabs
          value={aba}
          onChange={(_, v: number) => setAba(v)}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ borderBottom: 1, borderColor: "divider", px: 2 }}
        >
          {abas.map((label) => (
            <Tab key={label} label={label} />
          ))}
        </Tabs>

        <Box sx={{ px: 3 }}>
          {conteudo.map((secao, i) => (
            <TabPanel key={i} value={aba} index={i}>
              <SecaoGuia {...secao} />
            </TabPanel>
          ))}
        </Box>
      </Paper>
    </Box>
  );
}
