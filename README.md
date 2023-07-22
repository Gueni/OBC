# EV Onboard Charger with PFC and LLC Resonant Converter
## Overview

This repository contains the design and implementation of an Electric Vehicle (EV) Onboard Charger with Power Factor Correction (PFC) and LLC Resonant Converter. The onboard charger is responsible for efficiently converting AC power from the grid into DC power for charging the EV's battery pack.

The charger is designed to meet specific power requirements and comply with safety and regulatory standards. It utilizes PFC to improve power factor and LLC resonant converter for high efficiency and reduced switching losses.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [PCB Design](#pcb-design)
- [Control Circuit](#control-circuit)
- [How to Use](#how-to-use)
- [Safety and Compliance](#safety-and-compliance)

## Features

- High-efficiency power conversion with PFC and LLC resonant converter.
- Galvanic isolation between input and output using a transformer.
- Overvoltage, overcurrent, and overtemperature protection.
- Compliance with safety and regulatory standards.

## System Architecture

The EV Onboard Charger consists of two main sections: the Power Factor Correction (PFC) stage and the LLC Resonant Converter stage. PFC ensures high power factor and low harmonic distortion, while the LLC resonant converter improves overall efficiency.

## Project Structure

The repository is organized as follows:

|-- src/ # Source code for control circuit and firmware.
|-- pcb_design/ # PCB layout and design files.
|-- simulations/ # Simulations and performance analysis files.
|-- documentation/ # Project documentation and datasheets.
|-- examples/ # Example usage and test cases.
|-- LICENSE # License information.
|-- README.md # This README file.


## PCB Design

The `pcb_design/` directory contains all the files related to the PCB layout and design. It includes Gerber files, BOM (Bill of Materials), and schematic diagrams.

## Control Circuit

The `src/` directory contains the source code for the control circuitry and firmware of the onboard charger. The control circuit manages PFC and LLC converter operations, as well as the safety features.

## How to Use

To use the EV onboard charger, follow these steps:

1. Clone the repository: `git clone https://github.com/your_username/ev-onboard-charger.git`
2. Set up the development environment and build the control circuit firmware.
3. Fabricate the PCB design using the provided Gerber files.
4. Assemble the components onto the PCB.
5. Test the charger with a suitable input power source and EV battery pack.

## Safety and Compliance

The EV Onboard Charger is designed to meet safety and regulatory standards, including electrical isolation, thermal performance, and electromagnetic compatibility (EMC). Before using the charger, ensure that it complies with all relevant safety regulations in your region.
