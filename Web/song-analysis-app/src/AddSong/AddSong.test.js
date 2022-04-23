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

// make sure it is empty
it("input is initially empty", () => {
    render(<AddSong />, container);
    
    const inputEl = screen.getByRole('textbox');
    expect(inputEl.value).toBe('');
})

// no value inputted
it("error message shows up if no value is submitted", () => {
    render(<AddSong />, container);

    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('Not a valid link')).toBeTruthy();
})

// invalid link
it("error message shows up if an invalid link is submitted", () => {
    render(<AddSong />, container);

    const inputEl = screen.getByRole('textbox');

    fireEvent.change(inputEl, { target: { value: 'vg.no'}});
    fireEvent.click(screen.getByRole('button'));
    
    expect(screen.getByText('Not a valid link')).toBeTruthy();
})

// invalid link
it("error message shows up if an invalid link is submitted", () => {
    render(<AddSong />, container);

    const inputEl = screen.getByRole('textbox');

    fireEvent.change(inputEl, { target: { value: 'https://www.youtube.com/watch?v=Pzj3OiQjpmw' } });
    fireEvent.click(screen.getByRole('button'));

    expect(screen.getByText('Parsing link...')).toBeTruthy();
})