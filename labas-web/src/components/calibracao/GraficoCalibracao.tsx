import { useMemo } from "react";
import { Box, Typography } from "@mui/material";
import {
  ComposedChart,
  Scatter,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { PontoCalibracao } from "../../types/calibracao";

interface Props {
  pontos: PontoCalibracao[];
  a: number | null;
  b: number | null;
  r2: number | null;
  equacao: string;
  leituraLabel?: string;
}

const DIAMOND = (props: {
  cx?: number;
  cy?: number;
  fill?: string;
}) => {
  const { cx = 0, cy = 0, fill = "#1565c0" } = props;
  const size = 7;
  return (
    <polygon
      points={`${cx},${cy - size} ${cx + size},${cy} ${cx},${cy + size} ${cx - size},${cy}`}
      fill={fill}
      stroke={fill}
    />
  );
};

export function GraficoCalibracao({
  pontos,
  a,
  b,
  r2,
  equacao,
  leituraLabel = "Absorvância",
}: Props) {
  const { scatterData, lineData, xMax } = useMemo(() => {
    if (pontos.length < 2) return { scatterData: [], lineData: [], xMax: 10 };

    const scatter = pontos.map((p) => ({
      x: Number(p.concentracao),
      y: Number(p.absorvancia),
    }));

    const xs = scatter.map((p) => p.x);
    const maxX = Math.max(...xs);
    const computedXMax = maxX > 0 ? maxX * 1.15 : 10;

    // 60 pontos para uma linha suave
    const line =
      a !== null && b !== null
        ? Array.from({ length: 61 }, (_, i) => {
            const x = (computedXMax * i) / 60;
            return { x, y: Number(a) * x + Number(b) };
          })
        : [];

    return { scatterData: scatter, lineData: line, xMax: computedXMax };
  }, [pontos, a, b]);

  if (pontos.length < 2) return null;

  const r2Label =
    r2 !== null ? `R² = ${Number(r2).toFixed(4)}` : null;

  return (
    <Box>
      <Box
        display="flex"
        justifyContent="flex-end"
        alignItems="center"
        gap={2}
        mb={0.5}
        flexWrap="wrap"
      >
        <Typography variant="caption" fontFamily="monospace">
          {equacao}
        </Typography>
        {r2Label && (
          <Typography variant="caption" fontFamily="monospace">
            {r2Label}
          </Typography>
        )}
      </Box>

      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart margin={{ top: 5, right: 20, bottom: 20, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="x"
            type="number"
            domain={[0, xMax]}
            label={{ value: "Concentração (padrão)", position: "insideBottom", offset: -10 }}
            tickCount={6}
          />
          <YAxis
            type="number"
            label={{
              value: leituraLabel,
              angle: -90,
              position: "insideLeft",
              offset: 10,
            }}
          />
          <Tooltip
            formatter={(value: number, name: string) => [
              Number(value).toFixed(4),
              name,
            ]}
          />
          <Legend verticalAlign="top" />

          {lineData.length > 0 && (
            <Line
              data={lineData}
              dataKey="y"
              type="linear"
              stroke="#333333"
              strokeWidth={1.5}
              dot={false}
              name="Linear"
              legendType="line"
            />
          )}

          <Scatter
            data={scatterData}
            fill="#1565c0"
            name="Emissão"
            shape={<DIAMOND />}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </Box>
  );
}
