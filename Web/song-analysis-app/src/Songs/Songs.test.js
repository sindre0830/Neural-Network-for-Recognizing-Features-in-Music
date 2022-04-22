import { fireEvent, render, screen } from "@testing-library/react";
import { unmountComponentAtNode  } from "react-dom";
import { act } from "react-dom/test-utils";
import Songs from './Songs';

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

// fetching of songs
it("fetch songs", async () => {
    const results = [
        {
            Title: 'National Anthem - Lana Del Rey',
            Bpm: 130,
            Beats: [1.23,4.56,7.89],
            Chords: ['A','B','C'],
            Approved: false
        },
        {
            Title: 'Kaleidoscope - blink-182',
            Bpm: 120,
            Beats: [1.11,2.22],
            Chords: ['D','E'],
            Approved: true
        }
    ];

    jest.spyOn(global, 'fetch').mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(results)
        })
    );

    await act(async () => {
        render(<Songs />, container);
    });

    expect(screen.findByText('No songs have been added yet...')).toBeTruthy();

    global.fetch.mockRestore();
});

// no songs have been added yet
it("no songs have been added yet", async () => {
    const results = [];

    jest.spyOn(global, 'fetch').mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(results)
        })
    );

    await act(async () => {
        render(<Songs />, container);
    });

    expect(screen.findByText('Neatet')).toBeTruthy();

    global.fetch.mockRestore();
});
    