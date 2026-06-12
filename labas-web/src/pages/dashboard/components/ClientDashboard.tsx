import {
  Box,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  Paper,
  Typography,
} from "@mui/material";
import StatusChip from "../../../components/shared/StatusChip";
import type { Laudo } from "../../../types/analise";

interface Props {
  laudos: Laudo[];
  onBaixarPdf: (id: number, codigoLaudo: string) => void;
}

const formatarData = (value: string) => {
  const data = new Date(value);
  if (Number.isNaN(data.getTime())) {
    return value;
  }
  return data.toLocaleDateString("pt-BR");
};

const ordenarPorEntrada = (a: Laudo, b: Laudo) =>
  new Date(b.data_emissao).getTime() - new Date(a.data_emissao).getTime();

export default function ClientDashboard({ laudos, onBaixarPdf }: Props) {
  const recentes = [...laudos].sort(ordenarPorEntrada).slice(0, 5);

  return (
    <Grid container spacing={3}>
      <Grid size={{ xs: 12, md: 8 }}>
        <Paper sx={{ p: 3, mb: 3 }} variant="outlined">
          <Typography variant="h6" fontWeight={700} gutterBottom>
            Servicos do Laboratorio
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Analises quimicas e fisicas de solo, com laudos oficiais e
            acompanhamento direto pelo portal.
          </Typography>
        </Paper>

        <Paper sx={{ p: 3 }} variant="outlined">
          <Typography variant="h6" fontWeight={700} gutterBottom>
            Meus laudos mais recentes
          </Typography>
          <List disablePadding>
            {recentes.map((laudo) => {
              const status = laudo.data_saida ? "concluido" : "em_andamento";

              return (
                <ListItem
                  key={laudo.id}
                  divider
                  sx={{ px: 0, alignItems: "flex-start" }}
                  secondaryAction={
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => onBaixarPdf(laudo.id, laudo.codigo_laudo)}
                    >
                      Baixar PDF
                    </Button>
                  }
                >
                  <ListItemText
                    primary={
                      <Box
                        sx={{
                          display: "flex",
                          alignItems: "center",
                          gap: 1,
                          flexWrap: "wrap",
                        }}
                      >
                        <Typography variant="subtitle2" fontWeight={700}>
                          {laudo.codigo_laudo}
                        </Typography>
                        <StatusChip status={status} />
                      </Box>
                    }
                    secondary={`Entrada: ${formatarData(laudo.data_emissao)}`}
                  />
                </ListItem>
              );
            })}
            {recentes.length === 0 && (
              <ListItem sx={{ px: 0 }}>
                <ListItemText
                  primary="Nenhum laudo encontrado"
                  secondary="Quando houver laudos, eles aparecerao aqui."
                />
              </ListItem>
            )}
          </List>
        </Paper>
      </Grid>

      <Grid size={{ xs: 12, md: 4 }}>
        <Paper sx={{ p: 3 }} variant="outlined">
          <Typography variant="h6" fontWeight={700} gutterBottom>
            Suporte ao cliente
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Precisa de ajuda com seus laudos? Fale com nossa equipe.
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">Telefone: (34) 3232-0000</Typography>
            <Typography variant="body2">Email: suporte@labas.com.br</Typography>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}
