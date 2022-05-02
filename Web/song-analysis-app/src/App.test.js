import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

it('renders ', () => {
    render(
        <MemoryRouter>
            <App />
        </MemoryRouter>
    );
});
