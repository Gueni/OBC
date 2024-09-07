![python3.x](https://img.shields.io/badge/python-3.x-brightgreen.svg)[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)



# EV Onboard Charger with PFC and LLC Resonant Converter
## Overview

This repository contains the design and implementation of an Electric Vehicle (EV) single phase Onboard Charger with Power Factor Correction (PFC) and LLC Resonant Converter. The onboard charger is responsible for efficiently converting AC power from the grid into DC power for charging the EV's battery pack.

The charger is designed to meet specific power requirements and comply with safety and regulatory standards. It utilizes PFC to improve power factor and LLC resonant converter for high efficiency and reduced switching losses.

## Table of Contents

- [Features](#features)
- [Requirements and Specifications](#requirements-and-specifications)
- [System Architecture Design](#system-architecture-design)
- [PFC Design](#pfc-design)
- [LLC Resonant Converter Design](#llc-resonant-converter-design)
- [Magnetic Component Design](#magnetic-component-design)
- [Modeling and Simulation](#modeling-and-simulation)
- [Schematic Capture](#schematic-capture)
- [PCB Design](#pcb-design)
- [Control Circuit Design](#control-circuit-design)
- [Safety and Compliance](#safety-and-compliance)
- [Prototype Development and Testing](#prototype-development-and-testing)
- [Production and Manufacturing](#production-and-manufacturing)

## Features

- Electric Vehicle On-Board Charger (OBC) designed for efficient charging of 400/450 VDC batteries.
- Supports AC mains input voltage range of 90V - 265V (230V/110V) and DC charging input of 300V - 1000V.
- Outputs voltage of 250 - 450 VDC and 7 kW power, ensuring >96% efficiency and >0.96 power factor.
- Safety features include overcurrent, overvoltage, overtemperature, and short circuit protection, with galvanic isolation.
- Incorporates efficient cooling systems and communication interfaces like CAN and charging protocol.

## Requirements and Specifications

The requirements and specifications document outlines the functional and performance requirements of the EV onboard charger.

## System Architecture Design

The system architecture design defines the high-level structure and components of the EV onboard charger.

## PFC Design

The PFC design focuses on the Power Factor Correction stage of the onboard charger.

## LLC Resonant Converter Design

The LLC Resonant Converter design details the implementation of the LLC resonant converter stage.

## Magnetic Component Design

The magnetic component design covers the design and selection of transformers and inductors.

## Modeling and Simulation

Modeling and simulation involve using software tools to analyze and optimize the performance of the onboard charger.

## Schematic Capture

Schematic capture involves creating the electrical schematics of the onboard charger.

## PCB Design

The PCB design encompasses the layout and design of the printed circuit board for the onboard charger.

## Control Circuit Design

The control circuit design includes the development of control algorithms and firmware for managing PFC and LLC converter operations.

## Safety and Compliance

The EV Onboard Charger is designed to meet safety and regulatory standards, including electrical isolation, thermal performance, and electromagnetic compatibility (EMC). Before using the charger, ensure that it complies with all relevant safety regulations in your region.

## Prototype Development and Testing

Prototype development and testing involve building and testing a physical prototype of the onboard charger.

## Production and Manufacturing

Production and manufacturing cover the mass production and assembly of the onboard charger for commercial use.


## How to Use

To use the EV onboard charger, follow these steps:

1. Clone the repository: `git clone https://github.com/Gueni/OBC.git`
2. Set up the development environment and build the control circuit firmware.
3. Fabricate the PCB design using the provided Gerber files.
4. Assemble the components onto the PCB.
5. Test the charger with a suitable input power source and EV battery pack.

## Copyright and Licensing
-----
    Licensed under the GNU General Public License License, Version 3.0
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at GNU .

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

###### [Issues :Feel free to submit issues and enhancement requests.](https://github.com/Gueni/OBC/issues) 
###### [FAQ    :Feel free to join discussions.](https://github.com/Gueni/OBC/discussions)

