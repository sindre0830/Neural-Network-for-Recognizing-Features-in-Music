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

it("inputs are initally filled with song result", () => {
    const result = {
        Title: "As it was - Harry Styles",
        Bpm: 163,
        Beats: [1,2,3],
        Chords: ['A','B','C'],
        Approved: false
    };

    render(<Song value={result} />, container);

    // click the button to reveal results
    const buttonEl = screen.getByTestId('arrow-down');
    fireEvent.click(buttonEl);

    // check if the results are as expected
    const titleEl = screen.getByLabelText(/title/i);
    const bpmEl = screen.getByLabelText(/bpm/i);
    const beatsEl = screen.getByLabelText(/beats/i);
    const chordsEl = screen.getByLabelText(/chords/i);

    expect(titleEl.value).toBe(result.Title);
    expect(bpmEl.value).toBe(result.Bpm.toString());
    expect(beatsEl.value).toBe(result.Beats.toString());
    expect(chordsEl.value).toBe(result.Chords.toString());
})

it("approve button is present if the song is pending", () => {
    const result = {
        Title: "As it was - Harry Styles",
        Bpm: 163,
        Beats: [1,2,3],
        Chords: ['A','B','C'],
        Approved: false
    };

    render(<Song value={result} />, container);

    const buttonEl = screen.getByRole("button");
    expect(buttonEl).toBeTruthy();
}) 

it("approve button is not present if the song is approved", () => {
    const result = {
        Title: "As it was - Harry Styles",
        Bpm: 163,
        Beats: [1,2,3],
        Chords: ['A','B','C'],
        Approved: true
    };

    render(<Song value={result} />, container);

    const buttonEl = screen.queryByText(/approve/i);
    expect(buttonEl).toBeNull();
})
