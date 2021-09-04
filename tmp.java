private void setUpNewSensor(DatagramPacket handshakePacket, ByteBuffer data) throws IOException {
		System.out.println("[TrackerServer] Handshake recieved from " + handshakePacket.getAddress() + ":" + handshakePacket.getPort());
		InetAddress addr = handshakePacket.getAddress();
		TrackerConnection sensor;
		synchronized(trackers) {
			sensor = trackersMap.get(addr);
		}
		if(sensor == null) {
			boolean isOwo = false;
			data.getLong(); // Skip packet number
			int boardType = -1;
			int imuType = -1;
			int firmwareBuild = -1;
			StringBuilder firmware = new StringBuilder();
			byte[] mac = new byte[6];
			String macString = null;
			if(data.remaining() > 0) {
				if(data.remaining() > 3)
					boardType = data.getInt();
				if(data.remaining() > 3)
					imuType = data.getInt();
				if(data.remaining() > 3)
					data.getInt(); // MCU TYPE
				if(data.remaining() > 11) {
					data.getInt(); // IMU info
					data.getInt();
					data.getInt();
				}
				if(data.remaining() > 3)
					firmwareBuild = data.getInt();
				int length = 0;
				if(data.remaining() > 0)
					length = data.get() & 0xFF; // firmware version length is 1 longer than that because it's nul-terminated
				while(length > 0 && data.remaining() != 0) {
					char c = (char) data.get();
					if(c == 0)
						break;
					firmware.append(c);
					length--;
				}
				if(data.remaining() > mac.length) {
					data.get(mac);
					macString = String.format("%02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
				}
			}
			if(firmware.length() == 0) {
				firmware.append("owoTrack");
				isOwo = true;
			}
			IMUTracker imu = new IMUTracker("udp:/" + handshakePacket.getAddress().toString(), this);
			ReferenceAdjustedTracker<IMUTracker> adjustedTracker = new ReferenceAdjustedTracker<>(imu);
			trackersConsumer.accept(adjustedTracker);
			sensor = new TrackerConnection(imu, handshakePacket.getSocketAddress());
			sensor.isOwoTrack = isOwo;
			int i = 0;
			synchronized(trackers) {
				i = trackers.size();
				trackers.add(sensor);
				trackersMap.put(addr, sensor);
			}
			System.out.println("[TrackerServer] Sensor " + i + " added with address " + handshakePacket.getSocketAddress() + ". Board type: " + boardType + ", imu type: " + imuType + ", firmware: " + firmware + " (" + firmwareBuild + "), mac: " + macString);
		}
		sensor.tracker.setStatus(TrackerStatus.OK);
        socket.send(new DatagramPacket(HANDSHAKE_BUFFER, HANDSHAKE_BUFFER.length, handshakePacket.getAddress(), handshakePacket.getPort()));
	}