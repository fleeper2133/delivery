import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
  { field: 'tracking_number', headerName: 'Трек-номер', width: 150 },
  { field: 'transport_number', headerName: 'Номер ТС', width: 120 },
  { field: 'services', headerName: 'Услуга', width: 200 },
  { 
    field: 'delivery_date', 
    headerName: 'Дата доставки', 
    width: 150,
    valueFormatter: (params: { value: string }) => params.value || 'Не указана'  },
  { field: 'distance_km', headerName: 'Дистанция (км)', width: 130 },
  { 
    field: 'status', 
    headerName: 'Статус', 
    width: 150,
    valueFormatter: (params: { value: string }) => params.value || 'Не указан'
  }
];

interface DeliveriesTableProps {
  deliveries: Array<{
    id: number;
    tracking_number: string;
    transport_number: string;
    services: string;
    distance_km: number;
    delivery_date: string;
    status: string;
  }>;
}

export const DeliveriesTable = ({ deliveries }: DeliveriesTableProps) => (
  <div style={{ height: 600, width: '100%' }}>
    <DataGrid
      rows={deliveries}
      columns={columns}
      initialState={{
        pagination: {
          paginationModel: {
            pageSize: 10,
          },
        },
      }}
      pageSizeOptions={[10]}
    />
  </div>
);