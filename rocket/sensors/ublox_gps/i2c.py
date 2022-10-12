from smbus2 import SMBus

I2C_ADDRESS = 0x42
REG_BYTES_AVAIL = 0xFD

bus = SMBus(1)

bus.read_i2c_block_data()
