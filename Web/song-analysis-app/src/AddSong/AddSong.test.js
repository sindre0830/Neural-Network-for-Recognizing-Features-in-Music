import { fireEvent, render, screen } from "@testing-library/react";
import { unmountComponentAtNode  } from "react-dom";
import AddSong from './AddSong';

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

it('input is initially empty', () => {
    render(<AddSong />, container);
    
    const inputEl = screen.getByRole('textbox');
    expect(inputEl.value).toBe('');
})

describe('input validation', () => {
    it('error message shows up if no value is submitted', () => {
        render(<AddSong />, container);

        fireEvent.click(screen.getByRole('button'));
        expect(screen.getByText('Not a valid link')).toBeTruthy();
    })

    it('error message shows up if an invalid link is submitted', () => {
        render(<AddSong />, container);

        const inputEl = screen.getByRole('textbox');

        fireEvent.change(inputEl, { target: { value: 'vg.no' } });
        fireEvent.click(screen.getByRole('button'));

        expect(screen.getByText('Not a valid link')).toBeTruthy();
    })
})


it('parsing message shows up when valid link is submitted', () => {
    render(<AddSong />, container);

    const inputEl = screen.getByRole('textbox');

    fireEvent.change(inputEl, { target: { value: 'https://www.youtube.com/watch?v=Pzj3OiQjpmw' } });
    fireEvent.click(screen.getByRole('button'));

    expect(screen.getByText('Parsing link...')).toBeTruthy();
})
