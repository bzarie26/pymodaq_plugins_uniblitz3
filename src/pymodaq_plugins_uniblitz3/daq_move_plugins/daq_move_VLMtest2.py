from typing import Union, List, Dict

from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter
import serial
import serial.tools.list_ports
import sys

#class PythonWrapperOfYourInstrument:
     #TODO Replace this fake class with the import of the real python wrapper of your instrument
    #pass

# TODO:
# (1) change the name of the following class to DAQ_Move_TheNameOfYourChoice DID
# (2) change the name of this file to daq_move_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.) DID
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_move_plugins DID

class DAQ_Move_VLMtest2(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of controllers and actuators that should be compatible with this instrument plugin.
        * With which instrument and controller it has been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    is_multiaxes = False  # TODO for your plugin set to True if this plugin is controlled for a multiaxis controller DID
    _axis_names: Union[List[str], Dict[str, int]] = ['Axis1','Axis2']  # TODO for your plugin: complete the list I DON'T KNOW
    _controller_units: Union[str, List[str]] = ''  # TODO for your plugin: put the correct unit here, it could be
    # TODO  a single str (the same one is applied to all axes) or a list of str (as much as the number of axes)
    _epsilon: Union[float, List[float]] = 0.1  # TODO replace this by a value that is correct depending on your controller DID
    # TODO it could be a single float of a list of float (as much as the number of axes)
    data_actuator_type = DataActuatorType.DataActuator  # wether you use the new data style for actuator otherwise set this
    # as  DataActuatorType.float  (or entirely remove the line) DID I THINK
     
    def list_com_ports(): #list of available port
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    available_ports= list_com_ports()
    if len(available_ports) == 0:
        print('no available ports')
        sys.exit(1)
    else:
        params = [   {'title':'COM Port', 'name':'com_port', 'type': 'list', 'limits' : available_ports, 'value':available_ports[1] }
                ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)


    # _epsilon is the initial default value for the epsilon parameter allowing pymodaq to know if the controller reached DID
    # the target value. It is the developer responsibility to put here a meaningful value



    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy  
        #  autocompletion
        self.controller= None
        #self.controller: PythonWrapperOfYourInstrument = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = self.current_position       
        return pos

    def user_condition_to_reach_target(self) -> bool:
        """ Implement a condition for exiting the polling mechanism and specifying that the
        target value has been reached

       Returns
        -------
        bool: if True, PyMoDAQ considers the target value has been reached
        """
        # TODO either delete this method if the usual polling is fine with you, but if need you can
        #  add here some other condition to be fullfilled either a completely new one or
        #  using or/and operations between the epsilon_bool and some other custom booleans
        #  for a usage example see DAQ_Move_brushlessMotor from the Thorlabs plugin
        return True

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        if self.controller is not None:
            self.controller.close()
        else:
            print('no shutter has been initialized')
        #  self.controller.your_method_to_terminate_the_communication()  # when writing your own plugin replace this line

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings
    
        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        new_port=str(self.settings.child('com_port').value())
        try:
            self.controller=serial.Serial(new_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2, xonxoff=0, rtscts=0)
            print('ok')
        except serial.SerialException as e:
            print(f'connection failed: {e}')
            

        

    def ini_stage(self, controller=None):

        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
            
        """
        try:
            com_port=self.settings.child('com_port').value()
            self.controller= serial.Serial(com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2, xonxoff=0, rtscts=0)
            print('connecté')
            print(com_port)
            initialized=True
            info='initialisation sucess'
        except:
            info = 'initialisation failed'
            initialized =False


        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """



        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """
        # if value>0:
        #     value=1
        # else:
        #     value=0
        # if self.controller.is_open:
        #     print('open port')
        #     self.controller.write([b'A', b'@'][int(value)])
        #     self.current_position = int(value)
        #     self.get_actuator_value()
        # else:
        #     print('not open port') 
        print('yes')
        if self.controller.is_open:
            print('open port')
            if value==0:
                value=0
                self.controller.write(bytes([65]))
                print('ii')
            elif value==3:
                value=3
                self.controller.write(bytes([64]))
                print('oo')
            elif value ==1:
                value=1
                self.controller.write(bytes([128]))
                self.controller.write(bytes([145]))
                print('Io')
            elif value==2:
                value=2
                self.controller.write(bytes([129]))
                self.controller.write(bytes([144]))
                print('oI')
            else:
                print('out of bound')
            self.current_position = int(value)
            self.get_actuator_value()
        else:
            print('not open port')

    def move_rel(self, value: DataActuator):
        position= self.current_position + value
        self.move_abs(position)
        # if value>0:
        #     self.move_abs(1)
        # else:
        #     self.move_abs(0)
        

    def move_home(self):
        self.move_abs(0)



    def stop_motion(self):
      self.close()

      ## TODO for your custom plugin
      #raise NotImplemented  # when writing your own plugin remove this line
      #self.controller.your_method_to_stop_positioning()  # when writing your own plugin replace this line
      #self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


if __name__ == '__main__':
    main(__file__)
