import { useEffect, useState } from 'react';
import { Box, CircularProgress, Typography, Paper } from '@mui/material';
import apiClient from '../api/client';
import { Filters } from '../components/Filters';
import { DeliveryChart } from '../components/Chart';
import { DeliveriesTable } from '../components/DeliveriesTable';
import { format } from 'date-fns';

interface Delivery {
  id: number;
  tracking_number: string;
  transport_number: string;
  services: string;
  distance_km: number;
  status: { name: string } | string;
  actual_delivery: string;
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
    by_date?: Array<{ delivery_date: string; count: number }>;
  };
  deliveries?: Delivery[];
}

const ReportPage = () => {
  const [filters, setFilters] = useState<FiltersState>({
    dateFrom: null,
    dateTo: null,
    service: '',
    cargoType: '',
  });
  
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

        const [statsResponse, deliveriesResponse] = await Promise.all([
          apiClient.get('statistics/', { params: cleanParams }),
          apiClient.get('deliveries/', { params: cleanParams }),
        ]);

        setData({
          stats: statsResponse.data || {},
          deliveries: deliveriesResponse.data || [],
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
    status: typeof delivery.status === 'object' ? delivery.status?.name : delivery.status || 'Не указан',
    delivery_date: delivery.actual_delivery 
      ? format(delivery.actual_delivery, 'dd.MM.yyyy') 
      : 'Не указана'
  }));

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Отчет по доставкам
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Filters 
          filters={filters}
          setFilters={setFilters}
          services={[]}
          cargoTypes={[]}
        />
      </Paper>

      {data?.stats && (
        <>
          {data.stats.by_service && (
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Статистика доставок по услугам
              </Typography>
              <DeliveryChart 
                data={data.stats.by_service.map(item => ({
                  name: item.services__name,
                  count: item.count
                }))} 
              />
            </Paper>
          )}
          
          {data.stats.by_date && (
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Статистика доставок по датам
              </Typography>
              <DeliveryChart 
                data={data.stats.by_date.map(item => ({
                  name: format(item.delivery_date, 'dd.MM.yyyy'),
                  count: item.count
                }))}
              />
            </Paper>
          )}
        </>
      )}

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Таблица доставок
        </Typography>
        <DeliveriesTable deliveries={formattedDeliveries} />
      </Paper>
    </Box>
  );
};

export default ReportPage;