type Position = {x: number; y: number; z: number};
declare function world(x: number, y: number, z: number): Position;
declare const player: {
    say(s: string): void;
    position(): {getValue(a: number): number};
    onChat(command: string, callback: () => void): void;
};
declare const Axis: {X: number; Y: number; Z: number};
declare const AIR: number;
declare const STONE: number;
declare const GOLD_BLOCK: number;
declare const FillOperation: {Replace: number};
declare const CloneMask: {Replace: number};
declare const CloneMode: {Normal: number};
declare const TestForBlocksMask: {All: number};
declare const blocks: {
    testForBlock(id: number, position: Position): boolean;
    testForBlocks(a: Position, b: Position, dest: Position, mode: number): boolean;
    fill(id: number, a: Position, b: Position, mode: number): void;
    clone(a: Position, b: Position, dest: Position, mask: number, mode: number): boolean;
};
declare const file: {writeFile(path: string, content: string): void; readFile(path: string): string};
declare const loops: {pause(ms: number): void; runInBackground(fn: () => void): void};
