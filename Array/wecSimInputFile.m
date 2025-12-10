clear; close all;

%% PTO Data
inputs.CylDiam1 = 2.3771;
inputs.CylLength1 = 2.9850 ;
inputs.CylDiam2 = 1.8148;
inputs.CylLength2 = 2.7098 ;
inputs.CylDiam3 = 1.5734;
inputs.CylLength3 = 3.8491 ;
inputs.Pressure = 8.000e+05;
inputs.OrificeRatio = 0.2447;

% Recompute AOE struct and push it to base workspace
AOE = Constants_3Body_v2(inputs);

%% Simulation Data
simu = simulationClass();               % Initialize Simulation Class
simu.simMechanicsFile = 'AOE_OBAS.slx'; % Specify Simulink Model File
simu.mode = 'normal';                   % Specify Simulation Mode ('normal','accelerator','rapid-accelerator')
simu.explorer = 'on';                   % Turn SimMechanics Explorer (on/off)
simu.startTime = 0;                     % Simulation Start Time [s]
simu.rampTime = 100;                    % Wave Ramp Time [s]
simu.endTime = 200;                     % Simulation End Time [s]
simu.solver = 'ode4';                   % simu.solver = 'ode4' for fixed step & simu.solver = 'ode45' for variable step 
simu.dt = 0.01; 						% Simulation time-step [s]

%% Wave Information 

% noWave no waves 
waves = waveClass('noWave');            % Initialize Wave Class and Specify Type  
waves.period = 8;                       % Wave Period [s]

% % noWaveCIC, no waves with radiation CIC  
% waves = waveClass('noWaveCIC');       % Initialize Wave Class and Specify Type  
% waves.period = 8;                       % Wave Period [s]

% % Regular Waves  
% waves = waveClass('regular');           % Initialize Wave Class and Specify Type                                 
% waves.height = 0.5;                     % Wave Height [m]
% waves.period = 8;                       % Wave Period [s]

% % Regular Waves with CIC
% waves = waveClass('regularCIC');          % Initialize Wave Class and Specify Type                                 
% waves.height = 2.5;                       % Wave Height [m]
% waves.period = 8;                         % Wave Period [s]

% % Irregular Waves using PM Spectrum 
%  waves = waveClass('irregular');           % Initialize Wave Class and Specify Type
%  waves.height = 2.5;                       % Significant Wave Height [m]
%  waves.period = 8;                         % Peak Period [s]
%  waves.spectrumType = 'PM';                % Specify Wave Spectrum Type
%  waves.direction=[0];

% % Irregular Waves using JS Spectrum with Equal Energy and Seeded Phase
% waves = waveClass('irregular');           % Initialize Wave Class and Specify Type
% waves.height = 2.5;                       % Significant Wave Height [m]
% waves.period = 8;                         % Peak Period [s]
% waves.spectrumType = 'JS';                % Specify Wave Spectrum Type
% waves.bem.option = 'EqualEnergy';         % Uses 'EqualEnergy' bins (default) 
% waves.phaseSeed = 1;                      % Phase is seeded so eta is the same

% % Irregular Waves using PM Spectrum with Traditional and State Space 
% waves = waveClass('irregular');           % Initialize Wave Class and Specify Type
% waves.height = 2.5;                       % Significant Wave Height [m]
% waves.period = 8;                         % Peak Period [s]
% waves.spectrumType = 'PM';                % Specify Wave Spectrum Type
% simu.stateSpace = 1;                      % Turn on State Space
% waves.bem.option = 'Traditional';         % Uses 1000 frequnecies

% % Irregular Waves with imported spectrum
% waves = waveClass('spectrumImport');      % Create the Wave Variable and Specify Type
% waves.spectrumFile = 'spectrumData.mat';  % Name of User-Defined Spectrum File [:,2] = [f, Sf]

% % Waves with imported wave elevation time-history  
% waves = waveClass('elevationImport');          % Create the Wave Variable and Specify Type
% waves.elevationFile = 'elevationData.mat';     % Name of User-Defined Time-Series File [:,2] = [time, eta]

%% Body Data
% Float 1
body(1) = bodyClass('hydroData/OBAS.h5');
% body(1) = bodyClass('hydroData/AOE1.h5');
    % Create the body(1) Variable, Set Location of Hydrodynamic Data File 
    % and Body Number Within this File. 
body(1).geometryFile = 'geometry/float_geometry.stl';    % Location of Geometry File
% body(1).mass = 33384;
body(1).mass = 'equilibrium';
    % Body Mass. The 'equilibrium' Option Sets it to the Displaced Water 
    % Weight.
body(1).inertia = [280400.48 280400.48 488067.73];  % Moment of Inertia [kg*m^2]

% Spar/Plate 1
body(2) = bodyClass('hydroData/OBAS.h5');
% body(2) = bodyClass('hydroData/AOE1.h5');
body(2).geometryFile = 'geometry/spar_geometry.stl';
% body(2).mass = 74162;
body(2).mass = 'equilibrium';
body(2).inertia = [27460364.88 27460919.49 1243536.41];

% Float 2
body(3) = bodyClass('hydroData/OBAS.h5');
% body(3) = bodyClass('hydroData/AOE2.h5');
body(3).geometryFile = 'geometry/float_geometry.stl'; 
% body(3).mass = 33384;
body(3).mass = 'equilibrium';                   
body(3).inertia = [280400.48 280400.48 488067.73];
body(3).initial.displacement = [70 0 0];

% Spar/Plate 2
body(4) = bodyClass('hydroData/OBAS.h5');
% body(4) = bodyClass('hydroData/AOE2.h5');
body(4).geometryFile = 'geometry/spar_geometry.stl'; 
% body(4).mass = 74162;
body(4).mass = 'equilibrium';                   
body(4).inertia = [27460364.88 27460919.49 1243536.41];
body(4).initial.displacement = [70 0 0];

% Float 3
body(5) = bodyClass('hydroData/OBAS.h5');
% body(5) = bodyClass('hydroData/AOE3.h5');
body(5).geometryFile = 'geometry/float_geometry.stl'; 
% body(5).mass = 33384;
body(5).mass = 'equilibrium';                   
body(5).inertia = [280400.48 280400.48 488067.73];
body(5).initial.displacement = [140 0 0];

% Spar/Plate 3
body(6) = bodyClass('hydroData/OBAS.h5'); 
% body(6) = bodyClass('hydroData/AOE3.h5');
body(6).geometryFile = 'geometry/spar_geometry.stl'; 
% body(6).mass = 74162;
body(6).mass = 'equilibrium';                   
body(6).inertia = [27460364.88 27460919.49 1243536.41];
body(6).initial.displacement = [140 0 0];

%% PTO and Constraint Parameters
% Floating Joint 1
constraint(1) = constraintClass('Constraint1'); % Initialize Constraint Class for Constraint1
constraint(1).location = [0 0 0];               % Constraint Location [m]

% Floating Joint 2
constraint(2) = constraintClass('Constraint2'); % Initialize Constraint Class for Constraint2
constraint(2).location = [70 0 0];               % Constraint Location [m]

% Floating Joint 3
constraint(3) = constraintClass('Constraint3'); % Initialize Constraint Class for Constraint3
constraint(3).location = [140 0 0];               % Constraint Location [m]

% Translational PTO 1
pto(1) = ptoClass('PTO1');                      % Initialize PTO Class for PTO1
pto(1).stiffness = 0;                           % PTO Stiffness [N/m]
pto(1).damping = 0;                             % PTO Damping [N/(m/s)]
pto(1).location = [0 0 0];                      % PTO Location [m]

% Translational PTO 2
pto(2) = ptoClass('PTO2');                      % Initialize PTO Class for PTO2
pto(2).stiffness = 0;                           % PTO Stiffness [N/m]
pto(2).damping = 0;                             % PTO Damping [N/(m/s)]
pto(2).location = [70 0 0];                      % PTO Location [m]

% Translational PTO 3
pto(3) = ptoClass('PTO3');                      % Initialize PTO Class for PTO3
pto(3).stiffness = 0;                           % PTO Stiffness [N/m]
pto(3).damping = 0;                             % PTO Damping [N/(m/s)]
pto(3).location = [140 0 0];                      % PTO Location [m]