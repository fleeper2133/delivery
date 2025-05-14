import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend,
  Cell,
  LabelList
} from 'recharts';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

interface ChartData {
  name: string;
  count: number;
}

interface DeliveryChartProps {
  data: ChartData[];
  title: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

export const DeliveryChart = ({ data, title }: DeliveryChartProps) => {
  const theme = useTheme();
  
  // Сортируем данные по убыванию для лучшей визуализации
  const sortedData = [...data].sort((a, b) => b.count - a.count);
  
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <Typography 
        variant="h6" 
        align="center" 
        gutterBottom
        sx={{ 
          color: theme.palette.text.primary,
          marginBottom: '20px',
          fontWeight: '500'
        }}
      >
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={sortedData}
          layout="horizontal"
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
          barSize={30}
        >
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke={theme.palette.divider}
            vertical={false} // Только горизонтальные линии сетки
          />
          <XAxis 
            dataKey="name" 
            tick={{ fill: theme.palette.text.secondary }}
            interval={0}
            height={70}
            tickMargin={10}
            angle={0}
            textAnchor="end"
          />
          <YAxis 
            tick={{ fill: theme.palette.text.secondary }}
            label={{
              value: 'Количество доставок',
              angle: -90,
              position: 'insideLeft',
              fill: theme.palette.text.primary,
              style: { textAnchor: 'middle' }
            }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: theme.palette.background.paper,
              borderColor: theme.palette.divider,
              borderRadius: theme.shape.borderRadius,
              boxShadow: theme.shadows[3],
            }}
            formatter={(value: number) => [
              <span style={{ color: "#FFFFFF" }}>Количество доставок: {value}</span>, 
            ]}
            
          />
          <Legend 
            wrapperStyle={{
              paddingTop: '20px'
            }}
          />
          <Bar 
            dataKey="count" 
            name="Количество доставок"
            radius={[4, 4, 0, 0]}
            animationDuration={1500}
          >
            {sortedData.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={COLORS[index % COLORS.length]} 
              />
            ))}
            <LabelList 
              dataKey="count" 
              position="top" 
              fill={theme.palette.text.primary}
              formatter={(value: number) => `${value} шт`}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};