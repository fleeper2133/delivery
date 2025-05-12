import { Box, MenuItem, Select, TextField } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { SetStateAction } from 'react';

interface Service {
  id: number;
  name: string;
}

interface CargoType {
  id: number;
  name: string;
}

interface FiltersType {
  dateFrom: Date | null;
  dateTo: Date | null;
  service: string;
  cargoType: string;
}

interface FiltersProps {
  filters: FiltersType;
  setFilters: (value: SetStateAction<FiltersType>) => void;
  services: Service[];
  cargoTypes: CargoType[];
}

export const Filters = ({ 
  filters, 
  setFilters, 
  services, 
  cargoTypes 
}: FiltersProps) => (
  <LocalizationProvider dateAdapter={AdapterDateFns}>
    <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
      <DatePicker
        label="Дата от"
        value={filters.dateFrom}
        onChange={(date) => setFilters({ ...filters, dateFrom: date })}
        // renderInput={(params) => <TextField {...params} />}
      />
      <DatePicker
        label="Дата до"
        value={filters.dateTo}
        onChange={(date) => setFilters({ ...filters, dateTo: date })}
        // renderInput={(params) => <TextField {...params} />}
      />
      <Select
        value={filters.service}
        onChange={(e) => setFilters({ ...filters, service: e.target.value })}
        displayEmpty
      >
        <MenuItem value="">Все услуги</MenuItem>
        {services.map((service: Service) => (
          <MenuItem key={service.id} value={service.id}>
            {service.name}
          </MenuItem>
        ))}
      </Select>
      <Select
        value={filters.cargoType}
        onChange={(e) => setFilters({ ...filters, cargoType: e.target.value })}
        displayEmpty
      >
        <MenuItem value="">Все типы груза</MenuItem>
        {cargoTypes.map((cargoType: CargoType) => (
          <MenuItem key={cargoType.id} value={cargoType.id}>
            {cargoType.name}
          </MenuItem>
        ))}
      </Select>
    </Box>
  </LocalizationProvider>
);