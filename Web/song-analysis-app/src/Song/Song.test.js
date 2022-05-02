import { fireEvent, render, screen } from "@testing-library/react";
import { unmountComponentAtNode  } from "react-dom";
import Song from './Song';

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

// test data
const resultApproved = {
    title: "As it was - Harry Styles",
    bpm: 163,
    beats: [1, 2, 3],
    chords: ['A', 'B', 'C'],
    approved: true
};

const resultPending = {
    title: "We Used To Be Friends - The Dandy Warhols",
    bpm: 117.213,
    beats: [0.3123, 2.414],
    chords: ['A', 'C#'],
    approved: false
};

it('inputs are initally filled with song result', () => {
    render(<Song value={resultPending} />, container);

    // check if the results are as expected
    const titleEl = screen.getByLabelText(/title/i);
    const bpmEl = screen.getByLabelText(/bpm/i);
    const beatsEl = screen.getByLabelText(/beats/i);
    const chordsEl = screen.getByLabelText(/chords/i);

    expect(titleEl.value).toBe(resultPending.title);
    expect(bpmEl.value).toBe(resultPending.bpm.toString());
    expect(beatsEl.value).toBe(resultPending.beats.toString());
    expect(chordsEl.value).toBe(resultPending.chords.toString());
})

describe('button displaying', () => {
    it('approve button is present if the song is pending', () => {
        render(<Song value={resultPending} />, container);

        const buttonEl = screen.getByRole("button");
        expect(buttonEl).toBeTruthy();
    })

    it('approve button is not present if the song is approved', () => {
        render(<Song value={resultApproved} />, container);

        const buttonEl = screen.queryByText(/approve/i);
        expect(buttonEl).toBeNull();
    })
})

describe('input validation', () => {
    it('invalid bpm value is submitted', () => {
        render(<Song value={resultPending} />, container);
    
        // click toggle button
        const toggleBtnEl = screen.getByTestId('arrow-down');
        fireEvent.click(toggleBtnEl);
    
        // change value
        const inputEl = screen.getByLabelText(/bpm/i);
        fireEvent.change(inputEl, {target: {value: 'test'}});
    
        // click approve button
        const approveBtnEl = screen.queryByText(/approve/i);
        fireEvent.click(approveBtnEl);
    
        // look for error message
        expect(screen.getByText('Not a valid Bpm format')).toBeTruthy();
    })
    
    it('invalid beats value is submitted', () => {
        render(<Song value={resultPending} />, container);
    
        // click toggle button
        const toggleBtnEl = screen.getByTestId('arrow-down');
        fireEvent.click(toggleBtnEl);
    
        // change value
        const inputEl = screen.getByLabelText(/beats/i);
        fireEvent.change(inputEl, { target: { value: 'test' } });
    
        // click approve button
        const approveBtnEl = screen.queryByText(/approve/i);
        fireEvent.click(approveBtnEl);
    
        // look for error message
        expect(screen.getByText('Not a valid Beats format')).toBeTruthy();
    })
    
    it('invalid chords value is submitted', () => {
        render(<Song value={resultPending} />, container);
    
        // click toggle button
        const toggleBtnEl = screen.getByTestId('arrow-down');
        fireEvent.click(toggleBtnEl);
    
        // change value
        const inputEl = screen.getByLabelText(/chords/i);
        fireEvent.change(inputEl, { target: { value: 'A,E#' } });
    
        // click approve button
        const approveBtnEl = screen.queryByText(/approve/i);
        fireEvent.click(approveBtnEl);
    
        // look for error message
        expect(screen.getByText('Not a valid Chords format')).toBeTruthy();
    })
})

