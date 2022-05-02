import { render, screen } from "@testing-library/react";
import { unmountComponentAtNode } from "react-dom";
import StatusList from './StatusList';

let container = null;
beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});

const testResults = [
    'Prom Queen - Beach Bunny',
    'This is the day - The The'
];

it('displaying of status', async () => {
    render(<StatusList title='Failed Songs' value={testResults} status='failed' />, container);

    expect(screen.getByText('Prom Queen - Beach Bunny')).toBeTruthy();
    expect(screen.getByText('This is the day - The The')).toBeTruthy();
    expect(screen.getByText('Failed Songs')).toBeTruthy();
})
