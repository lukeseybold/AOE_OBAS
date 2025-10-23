function [AOE] = Constants_1Device(inputs)

%% Contants for the AOE simulink model
% please run this beforfe running the AOE simulink model. This script
% contains all the necessary ICs and constants for the simulink model to
% compile

% Constant                    Definition

% Rs                          Specific gass constant(J/(kg*K)
% gma                         Heat capacity ratio cp/cv
% AtmPressure                 Atmospheric pressure (Pa)
% WaterTemperature            Atmospheric temperature (K)
% Gain                        Gain used for changing some parameters down the line
% Damping                     Damping coefficient (kg/s)
% Diameter                    Diameter of the cross section (m)
% CrossSectionalArea          CrossSectionalArea (m^2)
% SurfaceArea                 The surface area of the volume surrounding the air mass. This used for heat transfer rate calculation purposes (m^2)                 
% Stiffness                   Stifness coefficient (N/m)
% Mass                        Mass of the check valve ball (kg)
% ExtensionLimit_Mechanical   Mechanical extension limit (m)
% ExtensionLimit_MassFlow     Maximum massflow distance threshold (m)
% HeatConvection              Heat convection coefficient with the sea water (W/K*m^2)
% EndStopDamping              Damping coefficient for the cylinder. Gets activated when it's in the Endstop region (kg/s)
% EndStopStiffness            Stiffness coefficient for the cylinder. Gets activated when it's in the Endstop region (N/m)
% LowEndLimit                 Buffer used to activate EndStopDamping & EndStopStiffness near the low end of the cylinder (m)
% HighEndLimit                Buffer used to activate EndStopDamping & EndStopStiffness near the high end of the cylinder (m)
% CoulombFrictionGain         The gain used to determine the value of the Coulomb friction force
% CoulombFrictionLimit        The saturation limit for the Coulomb friction (N)    
% InitialPistonPosition       Initial position of the piston in the cylider (m)
% InitialPressure             Initial pressure of the vessel (Pa)
% InitialTemperature          Initial temperatur of the vessel (K)
% InitialVolume               Initial volume of the vessel (m^3)
% InitialAirMass              Initial air mass of the vessel (kg)
% RegulatedPressure           Pressure threshold where the valve lets air through (Pa)
% ValveGate                   Indicates whether the gate is open (1) or closed (0)

% Simulink Block name         Definition

% InletCylinderOrifice        Air inlet orifice that connects the atmosphere to the cylinder
% InletCylinderCheckValve     Check valve that lets air flow in the cylider
% cylinder                    Main cylinder that pumps air to the thank
% Chamber1                    Chamber #1 of the main cylidner
% Chamber2                    Chamber #2 of the main cylidner
% Chamber1Chamber2Orifice     Orifice connects chamber #1 to chamber #2 
% Chamber1Chamber2CheckValve  Check valuve that lets air flow from chamber #1 to chamber #2
% Chamber2Chamber1Orifice     Orifice connects chamber #2 to chamber #1 
% Chamber2Chamber1CheckValve  Check valuve that lets air flow from chamber #2 to chamber #1
% OutletCylinderOrifice       Orifice connects the cylinder to the tank
% OutletCylinderCheckValve    Check valuve that lets air flow from the cylinder to the thank
% Tank                        Storage vessel for the comperessed air
% OutletTankOrifice           Orifice connects the tank to the next connected unit
% OutletTankCheckValve        Check valuve that lets air flow from the tank to the next connected unit

%% General Constants
AOE.Rs                  = 288;          % For dry air 
AOE.gma                 = 1.4;          % air cp/cv
AOE.AtmPressure         = 101.3e3;      % 1 atm
AOE.AtmTemperature      = 293;          % 20 C Temperature of the air
AOE.WaterTemperature    = 280;          % 7 C Temperature of the sea water      %Eric, Nov. 7/16
AOE.Cp                  = 1005;         %J / kgK for air @ 300 K          %Eric, Nov. 18/16
AOE.OrificeRatio        = inputs.OrificeRatio;                        %Eric, Nov. 25/16

%% Unit1.Cylinder

AOE.Unit1.Cylinder.Length               = inputs.CylLength1;
AOE.Unit1.Cylinder.Diameter             = inputs.CylDiam1;
AOE.Unit1.Cylinder.CrossSectionalArea   = 0.25*pi*(AOE.Unit1.Cylinder.Diameter)^2;
AOE.Unit1.Cylinder.HeatConvection       = 0.2;  %This was referenced by Helen, Nov. 8/16
AOE.Unit1.Cylinder.EndStopDamping       = 5*10^6;
AOE.Unit1.Cylinder.EndStopStiffness     = 5*10^7;
AOE.Unit1.Cylinder.LowEndLimit          = 0.05*AOE.Unit1.Cylinder.Length;
AOE.Unit1.Cylinder.HighEndLimit         = 0.05*AOE.Unit1.Cylinder.Length;
AOE.Unit1.Cylinder.CoulombFrictionLimit = 0.4*AOE.Unit1.Cylinder.Diameter*1E3;      %This was referenced by Helen, Nov. 8/16
AOE.Unit1.Cylinder.CoulombFrictionGain  = 100000;
AOE.Unit1.Cylinder.InitialOffset        = -1.333414;

%% Unit1.InletCylinderOrifice

AOE.Unit1.InletCylinderOrifice.Diameter                         = AOE.Unit1.Cylinder.Diameter*AOE.OrificeRatio; %Eric, Nov. 25/16 // Old value was: %0.35;
AOE.Unit1.InletCylinderOrifice.CrossSectionalArea               = 0.25*pi*(AOE.Unit1.InletCylinderOrifice.Diameter)^2;


%% Unit1.Chamber1

AOE.Unit1.Chamber1.InitialPistonPosition    = AOE.Unit1.Cylinder.Length/2;          %Eric, Nov. 25/16
AOE.Unit1.Chamber1.InitialPressure          = AOE.AtmPressure;
AOE.Unit1.Chamber1.InitialTemperature       = AOE.AtmTemperature;
AOE.Unit1.Chamber1.InitialVolume            = AOE.Unit1.Cylinder.CrossSectionalArea * AOE.Unit1.Chamber1.InitialPistonPosition;
AOE.Unit1.Chamber1.InitialAirMass           = AOE.Unit1.Chamber1.InitialPressure * AOE.Unit1.Chamber1.InitialVolume/(AOE.Rs*AOE.Unit1.Chamber1.InitialTemperature);

%% Unit1.Chamber1Chamber2Orifice

AOE.Unit1.Chamber1Chamber2Orifice.Diameter                          = AOE.Unit1.InletCylinderOrifice.Diameter; %Eric, Nov. 14/16  // Old value was: % 0.5*AOE.Unit1.InletCylinderOrifice.Diameter;
AOE.Unit1.Chamber1Chamber2Orifice.CrossSectionalArea                = 0.25*pi*(AOE.Unit1.Chamber1Chamber2Orifice.Diameter)^2;


%% Unit1.Chamber2

AOE.Unit1.Chamber2.InitialPistonPosition    = AOE.Unit1.Cylinder.Length - AOE.Unit1.Chamber1.InitialPistonPosition;
AOE.Unit1.Chamber2.InitialPressure          = AOE.Unit1.Chamber1.InitialPressure;
AOE.Unit1.Chamber2.InitialTemperature       = AOE.Unit1.Chamber1.InitialTemperature;
AOE.Unit1.Chamber2.InitialVolume            = AOE.Unit1.Cylinder.CrossSectionalArea * AOE.Unit1.Chamber2.InitialPistonPosition;
AOE.Unit1.Chamber2.InitialAirMass           = AOE.Unit1.Chamber2.InitialPressure * AOE.Unit1.Chamber2.InitialVolume/(AOE.Rs*AOE.Unit1.Chamber2.InitialTemperature);

%% Unit1.OutletCylinderOrifice

AOE.Unit1.OutletCylinderOrifice.Diameter                        = AOE.Unit1.InletCylinderOrifice.Diameter;
AOE.Unit1.OutletCylinderOrifice.CrossSectionalArea              = 0.25*pi*(AOE.Unit1.OutletCylinderOrifice.Diameter)^2;

%% Unit1.Tank

AOE.Unit1.Tank.InitialPressure      = AOE.Unit1.Chamber2.InitialPressure;
AOE.Unit1.Tank.InitialTemperature   = AOE.Unit1.Chamber2.InitialTemperature;
AOE.Unit1.Tank.NumAccumulators      = 6; %Eric, Nov. 21/16 (from AOE report)
AOE.Unit1.Tank.Radius               = 0.4572;  %Eric, Nov. 21/16 (from AOE report)
AOE.Unit1.Tank.LengthNoCaps         = 1.63;     %Eric, Nov. 21/16 (from AOE report)
AOE.Unit1.Tank.SurfaceArea          = AOE.Unit1.Tank.NumAccumulators*( AOE.Unit1.Tank.LengthNoCaps*pi*2*AOE.Unit1.Tank.Radius + 4*pi*AOE.Unit1.Tank.Radius );  %Changed by Eric, Nov. 18/16 in order to change tank to reflect data given by AOE
AOE.Unit1.Tank.Volume               = AOE.Unit1.Tank.NumAccumulators*( pi*(AOE.Unit1.Tank.Radius^2)*AOE.Unit1.Tank.LengthNoCaps + (4/3)*pi*(AOE.Unit1.Tank.Radius^3) ); %Changed by Eric, Nov. 18/16 in order to change tank to reflect data given by AOE
AOE.Unit1.Tank.InitialAirMass       = AOE.Unit1.Tank.InitialPressure * AOE.Unit1.Tank.Volume/(AOE.Rs*AOE.Unit1.Tank.InitialTemperature);
AOE.Unit1.Tank.HeatConvection       = AOE.Unit1.Cylinder.HeatConvection;

%% Unit1.OutletTankOrifice

AOE.Unit1.OutletTankOrifice.Diameter                        = AOE.Unit1.InletCylinderOrifice.Diameter ;
AOE.Unit1.OutletTankOrifice.CrossSectionalArea              = 0.25*pi*(AOE.Unit1.OutletTankOrifice.Diameter)^2;

AOE.Unit1.OutletTankCheckValve.CrackPressure                = inputs.Pressure; %Eric, Nov.7/16


