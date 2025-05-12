import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ChartData {
  name: string;
  count: number;
}

interface DeliveryChartProps {
  data: ChartData[];
}

export const DeliveryChart = ({ data }: DeliveryChartProps) => (
  <ResponsiveContainer width="100%" height={400}>
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip 
        formatter={(value) => [value, 'Количество доставок']}
        labelFormatter={(label) => `Дата: ${label}`}
      />
      <Bar dataKey="count" fill="#8884d8" />
    </BarChart>
  </ResponsiveContainer>
);