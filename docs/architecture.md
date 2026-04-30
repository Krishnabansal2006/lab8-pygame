# Project Architecture

This document describes the architecture of the Pygame square simulation implemented in `main.py`.

## Scope

- Single Python module: `main.py`
- Main runtime loop driven by Pygame
- Two domain entities: `Square` and `Particle`
- Factory helpers for square creation and particle effects

## 1) Dependency Graph (Modules)

```mermaid
graph TD
    subgraph "Project Module"
        M["main.py"]
    end

    subgraph "Standard Library"
        R["random"]
        T["math"]
    end

    subgraph "Third-Party"
        P["pygame"]
    end

    subgraph "Runtime Objects"
        SQ["Square"]
        PT["Particle"]
        LOOP["Main Loop"]
    end

    M --> R
    M --> T
    M --> P
    M --> SQ
    M --> PT
    M --> LOOP
```

## 2) High-Level Runtime Flow

```mermaid
flowchart TD
    A["Program Start"] --> B["main()"]
    B --> C["Initialize pygame, window, clock, font"]
    C --> D["Create initial squares"]
    D --> E["Enter frame loop while running"]
    E --> F["Compute dt and current_time"]
    F --> G["Process QUIT events"]
    G --> H["Update each square"]
    H --> I["Death or caught check"]
    I --> J["Emit death particles and schedule rebirth"]
    I --> K["Keep square alive"]
    J --> L["Swap squares with alive list"]
    K --> L
    L --> M["Spawn due rebirths and birth particles"]
    M --> N["Draw squares"]
    N --> O["Update and draw particles"]
    O --> P["Render HUD and flip display"]
    P --> E
    E --> Q["Exit loop"]
    Q --> R["pygame.quit()"]
```

## 3) Function-Level Call Graph

```mermaid
graph TD
    subgraph "Entry"
        MAIN["main()"]
    end

    subgraph "Factories"
        CSQ["create_square(screen_w, screen_h)"]
        CSQS["create_squares(n, screen_w, screen_h)"]
        CDP["create_death_particles(x, y, color)"]
        CBP["create_birth_particles(x, y, color)"]
    end

    subgraph "Square Methods"
        SINIT["Square.__init__(x, y, size, color)"]
        SUPD["Square.update(screen_w, screen_h, squares, dt)"]
        SDEAD["Square.is_dead()"]
        SCAUGHT["Square.is_caught(squares)"]
        SDRAW["Square.draw(surface)"]
    end

    subgraph "Particle Methods"
        PINIT["Particle.__init__(x, y, color)"]
        PUPD["Particle.update(dt)"]
        PDEAD["Particle.is_dead()"]
        PDRAW["Particle.draw(surface)"]
    end

    MAIN --> CSQS
    CSQS --> CSQ
    CSQ --> SINIT

    MAIN --> SUPD
    MAIN --> SDEAD
    MAIN --> SCAUGHT
    MAIN --> SDRAW

    MAIN --> CDP
    CDP --> PINIT

    MAIN --> CBP
    CBP --> PINIT

    MAIN --> PDEAD
    MAIN --> PUPD
    MAIN --> PDRAW
```

## 4) Primary Execution Sequence (Full Frame Path)

```mermaid
sequenceDiagram
    participant U as "User"
    participant App as "main()"
    participant PG as "pygame"
    participant S as "Square"
    participant Part as "Particle"

    U->>App: "Run program"
    App->>PG: "init(), set_mode(), set_caption()"
    App->>App: "create_squares(NUM_SQUARES, WIDTH, HEIGHT)"
    loop "Each frame while running"
        App->>PG: "clock.tick(FPS)"
        App->>PG: "event.get()"
        alt "QUIT event found"
            App->>App: "running = False"
        else "No quit event"
            App->>PG: "screen.fill(BG_COLOR)"
            loop "For each square"
                App->>S: "update(WIDTH, HEIGHT, squares, dt)"
                App->>S: "is_dead()"
                App->>S: "is_caught(squares)"
                alt "Dead or caught"
                    App->>App: "create_death_particles(cx, cy, color)"
                    App->>Part: "Particle.__init__() x30"
                    App->>App: "pending_spawns.append(current_time + 2.0, cx, cy)"
                else "Alive"
                    App->>App: "append square to alive list"
                end
            end
            App->>App: "squares = alive"

            loop "For each pending spawn"
                alt "spawn_time reached"
                    App->>S: "Square.__init__(birth_x, birth_y, size, color)"
                    App->>App: "create_birth_particles(bx, by, color)"
                    App->>Part: "Particle.__init__() x30"
                    App->>App: "append new square"
                else "Not ready"
                    App->>App: "keep in still_pending"
                end
            end

            loop "Draw squares"
                App->>S: "draw(screen)"
            end

            App->>Part: "filter by is_dead()"
            loop "For each live particle"
                App->>Part: "update(dt)"
                App->>Part: "draw(screen)"
            end

            App->>PG: "font.render() and screen.blit()"
            App->>PG: "display.flip()"
        end
    end
    App->>PG: "quit()"
```

## Notes

- The project is intentionally centralized in one module (`main.py`), so coupling between game loop and entity logic is direct.
- Lifecycles are time-driven (`dt` and `current_time`) for frame-rate independent behavior.
- Rebirth is event-scheduled through `pending_spawns`, separated from immediate death handling.

## Assumptions

- The primary execution path is the `main()` loop in `main.py`.
- README currently mentions 20 squares, while code constant `NUM_SQUARES` is 15; diagrams reflect the code path, not README text.
