import { fireEvent, render, screen } from "@testing-library/react";
import { unmountComponentAtNode } from "react-dom";
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

const testResults = [
    {
        title: 'National Anthem - Lana Del Rey',
        bpm: 130,
        beats: [1.23, 4.56, 7.89],
        chords: ['A', 'B', 'C'],
        approved: false
    },
    {
        title: 'Kaleidoscope - blink-182',
        bpm: 120,
        beats: [1.11, 2.22],
        chords: ['D', 'E'],
        approved: true
    }
];

describe('displaying of results', () => {
    it('all songs are displayed', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(testResults)
            })
        );
    
        await act(async () => {
            render(<Songs />, container);
        });
    
        expect(screen.getByText('National Anthem - Lana Del Rey')).toBeTruthy();
        expect(screen.getByText('Kaleidoscope - blink-182')).toBeTruthy();
    
        global.fetch.mockRestore();
    })
    
    it('all results are displayed', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(null)
            })
        );
    
        await act(async () => {
            render(<Songs />, container);
        });
    
        expect(screen.getByText('No songs have been added yet...')).toBeTruthy();
    
        global.fetch.mockRestore();
    })
})

describe('searching and filtering', () => {
    it('searching for a song only returns that one song', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(testResults)
            })
        );

        await act(async () => {
            render(<Songs />, container);
        });

        // search for a song
        const searchEl = screen.getByPlaceholderText('Search for something...');
        fireEvent.change(searchEl, { target: { value: 'Lana Del Rey'}});

        expect(screen.queryByText('National Anthem - Lana Del Rey')).toBeTruthy();
        expect(screen.queryByText('Kaleidoscope - blink-182')).toBeNull();

        global.fetch.mockRestore();
    })

    it('filtering approved', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(testResults)
            })
        );

        await act(async () => {
            render(<Songs />, container);
        });

        // click the approved button
        const approvedEl = screen.getByLabelText('Approved');
        fireEvent.click(approvedEl);

        expect(screen.queryByText('National Anthem - Lana Del Rey')).toBeNull();
        expect(screen.queryByText('Kaleidoscope - blink-182')).toBeTruthy();

        global.fetch.mockRestore();
    })

    it('filtering pending', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(testResults)
            })
        );

        await act(async () => {
            render(<Songs />, container);
        });

        // click the pending button
        const pendingEl = screen.getByLabelText('Pending');
        fireEvent.click(pendingEl);

        // make sure the correct songs exists
        expect(screen.queryByText('National Anthem - Lana Del Rey')).toBeTruthy();
        expect(screen.queryByText('Kaleidoscope - blink-182')).toBeNull();

        global.fetch.mockRestore();
    })

    it('filtering all', async () => {
        jest.spyOn(global, 'fetch').mockImplementation(() =>
            Promise.resolve({
                json: () => Promise.resolve(testResults)
            })
        );

        await act(async () => {
            render(<Songs />, container);
        });

        // click the all button
        const allEl = screen.getByLabelText('All');
        fireEvent.click(allEl);

        // make sure the correct songs exists
        expect(screen.queryByText('National Anthem - Lana Del Rey')).toBeTruthy();
        expect(screen.queryByText('Kaleidoscope - blink-182')).toBeTruthy();

        global.fetch.mockRestore();
    })
})
