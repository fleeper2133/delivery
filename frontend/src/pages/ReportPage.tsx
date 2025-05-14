import { useEffect, useState } from 'react';
import { 
  Box, 
  CircularProgress, 
  Typography, 
  Paper, 
  MenuItem, 
  Select, 
  FormControl, 
  InputLabel,
  Button,
  Stack,
  AppBar,
  Toolbar,
  Container
} from '@mui/material';
import apiClient from '../api/client';
import { Filters } from '../components/Filters';
import { DeliveryChart } from '../components/Chart';
import { DeliveriesTable } from '../components/DeliveriesTable';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';

interface Delivery {
  id: number;
  tracking_number: string;
  transport_number: string;
  services: string;
  distance_km: number;
  status: { name: string };
  actual_delivery: string;
  scheduled_delivery: string;
}

interface FiltersState {
  dateFrom: Date | null;
  dateTo: Date | null;
  service: string;
  cargoType: string;
}

interface ApiData {
  stats: {
    total_deliveries?: number;
    total_distance_km?: number;
    total_revenue?: number;
    by_status?: Array<{ status__name: string; count: number }>;
    by_service?: Array<{ services__name: string; count: number }>;
    by_date?: Array<{ date: string; count: number }>;
  };
  deliveries?: Delivery[];
  allServices: [];
  allTypes: [];
}

type ChartType = 'by_date' | 'by_service' | 'by_status';

const ReportPage = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FiltersState>({
    dateFrom: null,
    dateTo: null,
    service: '',
    cargoType: '',
  });
  
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedChart, setSelectedChart] = useState<ChartType>('by_date');

  const handleLogout = () => {
    // Здесь должна быть логика выхода
    // Например, очистка токена, перенаправление и т.д.
    navigate('/login'); // Перенаправляем на страницу входа
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const params = {
          date_from: filters.dateFrom?.toISOString().split('T')[0],
          date_to: filters.dateTo?.toISOString().split('T')[0],
          service_id: filters.service || undefined,
          cargo_type_id: filters.cargoType || undefined,
        };
        
        const cleanParams = Object.fromEntries(
          Object.entries(params).filter(([_, value]) => value !== undefined)
        );

        const [statsResponse, deliveriesResponse, allServicesResponse, allTypesResponse] = await Promise.all([
          apiClient.get('statistics/', { params: cleanParams }),
          apiClient.get('deliveries/', { params: cleanParams }),
          apiClient.get('services/'),
          apiClient.get('cargo-types/')
        ]);

        setData({
          stats: statsResponse.data || {},
          deliveries: deliveriesResponse.data || [],
          allServices: allServicesResponse.data || [],
          allTypes: allTypesResponse.data || [],
        });
      } catch (err) {
        setError('Ошибка загрузки данных');
        console.error('Ошибка при загрузке данных:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  // Форматируем данные для таблицы
  const formattedDeliveries = (data?.deliveries || []).map(delivery => ({
    ...delivery,
    status:  delivery.status?.name,
    delivery_date: delivery.scheduled_delivery 
      ? format(delivery.scheduled_delivery, 'dd.MM.yyyy') 
      : 'Не указана'
  }));

  const renderSelectedChart = () => {
    if (!data?.stats) return null;

    switch (selectedChart) {
      case 'by_date':
        if (!data.stats.by_date) return null;
        return (
          <DeliveryChart 
            data={data.stats.by_date.map(item => ({
              name: format(item.date, 'dd.MM.yyyy'),
              count: item.count
            }))}
            title="Статистика доставок по датам"
          />
        );
      case 'by_service':
        if (!data.stats.by_service) return null;
        return (
          <DeliveryChart 
            data={data.stats.by_service.map(item => ({
              name: item.services__name,
              count: item.count
            }))} 
            title="Статистика доставок по услугам"
          />
        );
      case 'by_status':
        if (!data.stats.by_status) return null;
        return (
          <DeliveryChart 
            data={data.stats.by_status.map(item => ({
              name: item.status__name,
              count: item.count
            }))} 
            title="Статистика доставок по статусам"
          />
        );
      default:
        return null;
    }
  };

  return (
    <>
      <AppBar position="static" color="default" elevation={0}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Отчет по доставкам
          </Typography>
          <Button 
            variant="outlined" 
            color="inherit"
            onClick={handleLogout}
          >
            Выйти
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Filters 
            filters={filters}
            setFilters={setFilters}
            services={data?.allServices || []}
            cargoTypes={data?.allTypes || []}
          />
        </Paper>

        {data?.stats && (
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel id="chart-select-label">Тип графика</InputLabel>
              <Select
                labelId="chart-select-label"
                value={selectedChart}
                label="Тип графика"
                onChange={(e) => setSelectedChart(e.target.value as ChartType)}
              >
                <MenuItem value="by_date">По датам</MenuItem>
                <MenuItem value="by_service">По услугам</MenuItem>
                <MenuItem value="by_status">По статусам</MenuItem>
              </Select>
            </FormControl>
            
            {renderSelectedChart()}
          </Paper>
        )}

        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Таблица доставок
          </Typography>
          <DeliveriesTable deliveries={formattedDeliveries} />
        </Paper>
      </Container>
    </>
  );
};

export default ReportPage;