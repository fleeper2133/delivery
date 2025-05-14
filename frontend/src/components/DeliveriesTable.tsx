import { DataGrid, GridColDef } from '@mui/x-data-grid';

const columns: GridColDef[] = [
  { field: 'tracking_number', headerName: 'Трек-номер', width: 150 },
  { field: 'transport', headerName: 'Транспорт', width: 150, valueFormatter: (params: { name: string }) => params.name || 'Не указан' },
  { field: 'transport_number', headerName: 'Номер ТС', width: 120 },
  { field: 'services', headerName: 'Услуги', width: 200, valueFormatter: (params:  { name: string }[] ) => params.map(service => service.name).join(', ') || 'Не указан' },  { 
    field: 'delivery_date', 
    headerName: 'Дата доставки', 
    width: 150,
    valueFormatter: (params: { value: string }) => params || 'Не указана'  },
 
  { field: 'cargo_type', headerName: 'Тип груза', width: 150, valueFormatter: (params: { name: string }) => params?.name || 'Не указан' },
  { 
    field: 'status', 
    headerName: 'Статус', 
    width: 150,
    valueFormatter: (params: { value: string }) => params || 'Не указан'
  },
   { field: 'distance_km', headerName: 'Дистанция (км)', width: 130 },
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