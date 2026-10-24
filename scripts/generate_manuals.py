import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, getattr(self, 'doc_title', 'Product User Manual'))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "Official Documentation")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        
        self.drawString(54, 32, "Confidential & Proprietary - Helpdesk Technical Operations")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

PRODUCTS = [
    {
        "name": "Quantum Processor 9",
        "file_name": "quantum_processor_9_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$499.99",
        "model_no": "QP-9000-X",
        "sections": {
            "basic_info": (
                "The Quantum Processor 9 is an enterprise-grade auxiliary quantum co-processing unit engineered for high-throughput "
                "scientific computing, cryptographic simulations, and advanced tensor operations. Built on a proprietary 128-qubit logical "
                "simulation architecture, the processor operates seamlessly alongside standard x86 and ARM server architectures via a "
                "high-bandwidth PCIe 5.0 x16 slot. The unit features an active cryogenic vapor-chamber heat spreader, integrated error-correction "
                "hardware pipelines, and dual 8-pin supplemental power connectors capable of sustaining an 85W continuous TDP. Equipped with "
                "hardened low-noise shielding and ultra-low jitter phase-locked loops, the Quantum Processor 9 ensures sub-picosecond phase "
                "stability across intensive calculations, delivering over twenty times the matrix processing efficiency of conventional silicon accelerators."
            ),
            "how_to_use": (
                "To install and configure the Quantum Processor 9, adhere strictly to electrostatic discharge (ESD) safety protocols before opening "
                "your chassis. First, disconnect main system power and seat the card firmly into an unobstructed PCIe 5.0 x16 expansion slot. Secure "
                "the retention bracket with the provided chassis screw and attach two dedicated 8-pin PCIe power cables directly from a certified power supply. "
                "Next, power on the host system and verify that the diagnostic LED shifts from amber to solid teal. In your host operating environment "
                "(Linux kernel 5.15+ or Windows Server 2022+), download and install the Quantum Driver Suite v4.2. Run the initialization utility using "
                "'qp-init --calibrate' to tune coherence clocks and run thermal baselines. Once verification completes, launch your target runtime or container "
                "service; the driver exposes standard OpenCL and Q-Tensor APIs for rapid deployment across high-performance compute clusters."
            ),
            "troubleshooting": (
                "When experiencing operating anomalies with the Quantum Processor 9, consult the following diagnostic steps. Issue 1: Host fails to detect the card on boot. "
                "Resolution: Verify that PCIe slot bifurcation is configured correctly in host BIOS/UEFI, inspect the auxiliary power cables for secure latching, and "
                "ensure motherboard firmware is updated to the latest vendor revision. Issue 2: Qubit decoherence error or high calculation variance. Resolution: Check the chassis grounding wire "
                "and verify that electromagnetic interference sources such as unshielded high-voltage transformers are placed at least two feet away from the enclosure. "
                "Issue 3: Thermal throttling or diagnostic LED flashing red. Resolution: Inspect the vapor chamber intake for dust buildup, ensure ambient temperatures "
                "remain below 32°C, and review fan curve presets in the control panel to ensure adequate chassis airflow."
            ),
            "warranty": (
                "This product is backed by a strictly enforced 1-month (30-day) limited manufacturer warranty commencing from the documented date of delivery. "
                "Warranty coverage encompasses material defects in the silicon matrix, internal firmware controller malfunctions, and soldering structural failures under "
                "standard operating conditions. Coverage explicitly excludes damage resulting from unauthorized voltage modification, liquid ingress, physical shock, "
                "sub-zero condensation, or improper power supply regulation. To submit a warranty claim within the 1-month period, contact Helpdesk Technical Support "
                "at support@agentichelpdesk.com with your serial number, proof of purchase, and exported error diagnostic dump. Eligible units will receive replacement "
                "or factory refurbishment following RMA authorization."
            )
        }
    },
    {
        "name": "Holo-Projector Lite",
        "file_name": "holo_projector_lite_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$299.50",
        "model_no": "HPL-300-VOL",
        "sections": {
            "basic_info": (
                "The Holo-Projector Lite is a portable spatial holographic projection terminal designed to render true volumetric 3D imagery "
                "directly into mid-air without requiring specialized eyewear or projection screens. Featuring a precision micro-laser diode array combined with a "
                "high-speed optical refraction prism, it outputs 4K equivalent spatial voxel resolution across a generous 180-degree hemispherical viewing angle. "
                "The hardware integrates dual spatial audio speakers (5W RMS each) that sync acoustic wavefronts directly with projected imagery. With "
                "comprehensive connectivity including Wi-Fi 6E, Bluetooth 5.3, HDMI 2.1, and 100W USB-C Power Delivery, the Holo-Projector Lite bridges "
                "the gap between creative multimedia production, interactive architectural modeling, rapid engineering design reviews, and immersive telepresence conferencing."
            ),
            "how_to_use": (
                "Operating the Holo-Projector Lite requires minimal setup. Place the projector on a stable, level surface in an indoor setting with moderate "
                "to low ambient lighting for optimal contrast. Connect the supplied 100W USB-C fast charger into the power port. Depress the power button for "
                "two seconds until the illuminated perimeter ring glows azure. Pair the device with your laptop, smartphone, or workstation using the HoloSync app "
                "or connect directly via the high-speed HDMI input. Use the tactile rotary dial on top of the projector to adjust spatial depth focus until the "
                "floating calibration cube aligns sharply in the air. To stream content, drag compatible OBJ, glTF, or spatial video formats into the streaming window, "
                "and manage viewing angles via touch gestures in the companion software or through the included infrared remote control."
            ),
            "troubleshooting": (
                "If you encounter technical issues during projection, execute the following troubleshooting protocols. Issue 1: Projected hologram appears "
                "blurry, fragmented, or flickers intermittently. Resolution: Gently wipe the top optical refraction glass with the included anti-static microfiber "
                "cloth, verify there are no harsh direct spotlights striking the lens, and adjust the focal depth dial. Issue 2: Audio playback is unsynchronized "
                "with the 3D visual stream. Resolution: Re-pair the Bluetooth connection or switch from wireless casting to direct HDMI 2.1 cable mode to minimize "
                "latency. Issue 3: Projector suddenly powers down during rendering. Resolution: Check for ventilation blockages around the base cooling intake; if the "
                "overheat safety sensor tripped, allow the unit 15 minutes to cool before restarting at reduced ambient room temperature. Always ensure air filters are clean."
            ),
            "warranty": (
                "The Holo-Projector Lite includes a comprehensive 1-month (30-day) limited hardware warranty valid from the verified delivery date. The warranty "
                "protects against factory defects in laser projection assemblies, optical emitter failures, internal power board defects, and integrated wireless module "
                "malfunctions. Damage caused by drops, scratches on the prism glass, liquid immersion, or using uncertified power adapters is strictly excluded from "
                "warranty protection. For warranty claims or technical RMA processing within the 1-month period, email our customer service desk at support@agentichelpdesk.com. "
                "Please provide your transaction receipt, device serial number, and a brief video documenting the optical failure to initiate prompt return processing."
            )
        }
    },
    {
        "name": "Neural Link Headset",
        "file_name": "neural_link_headset_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$150.00",
        "model_no": "NLH-150-EEG",
        "sections": {
            "basic_info": (
                "The Neural Link Headset is an advanced consumer-accessible electroencephalographic (EEG) and electromyographic (EMG) interface designed "
                "for touchless human-computer interaction, cognitive biometric feedback, and mental state monitoring. Engineered with 16 dry-contact biopotential "
                "sensors made of conductive medical-grade gold alloy, the headset captures microvolt-level cortical signals across frontal, temporal, and parietal lobes. "
                "It features an adjustable ergonomic spring-steel chassis lined with memory foam, a 24-bit analog-to-digital converter, and an ultra-low latency "
                "Bluetooth 5.4 Low Energy transmitter. Powered by an internal 500mAh lithium-polymer battery delivering up to 18 hours of continuous bio-signal streaming, "
                "the headset sets a new benchmark for comfortable, gel-free neural computing in gaming, accessibility, research, and focus tracking applications."
            ),
            "how_to_use": (
                "Getting started with the Neural Link Headset involves fitting and rapid software calibration. Begin by gently sliding the adjustable headband "
                "over your head so that the front contact array sits roughly 2 centimeters above your eyebrows and the lateral pods make firm contact with the scalp "
                "behind your ears. Ensure natural hair is parted slightly beneath the sensors to maximize direct skin contact. Switch the power toggle to the 'ON' position; "
                "the status LED will flash green. Open the NeuralLink Studio app on your PC or mobile device and pair via Bluetooth. Sit comfortably and follow the on-screen "
                "3-minute baseline cognitive calibration routine, maintaining steady eye contact with the focus dot while the software builds your unique mental signal baseline. "
                "Once calibrated, assign specific facial gestures or focus states to custom keyboard and mouse macros."
            ),
            "troubleshooting": (
                "Refer to these standard remedies if signal acquisition or connection problems occur. Issue 1: High sensor impedance or erratic signal noise reading in the app. "
                "Resolution: Readjust sensor contact points on the scalp, lightly clean the gold sensor pins with a dry cotton swab, and ensure you are not situated directly "
                "adjacent to high-power unshielded power supplies or microwave emitters. Issue 2: Bluetooth connectivity drops or fails to pair. Resolution: Toggle device "
                "power, forget previous Bluetooth pairings on the host operating system, and recharge the headset battery to above 25%. Issue 3: Inaccurate gesture or command "
                "detection. Resolution: Re-run the cognitive baseline calibration routine while resting in a quiet, distraction-free environment without excessive jaw clenching."
            ),
            "warranty": (
                "The Neural Link Headset comes with a 1-month limited manufacturer warranty covering all internal circuit components, biopotential converter boards, "
                "and factory wireless transmitters for a period of 30 calendar days from the date of purchase. This warranty does not cover normal wear on headband padding, "
                "cosmetic abrasions, corrosion caused by sweat or moisture exposure beyond IPX4 ratings, or physical breakage of the flexible sensor arms due to excessive bending. "
                "To initiate a warranty assessment within the 1-month warranty window, submit a service ticket to support@agentichelpdesk.com along with purchase verification "
                "and an app telemetry export illustrating sensor failure. Authorized claims will receive rapid unit replacement."
            )
        }
    },
    {
        "name": "Plasma Battery Pack",
        "file_name": "plasma_battery_pack_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$45.99",
        "model_no": "PBP-25K-65W",
        "sections": {
            "basic_info": (
                "The Plasma Battery Pack is a high-density, ultra-durable 25,000mAh external power station built for power users, field technicians, and "
                "demanding multi-device workflows. Constructed with solid-state plasma-ion pouch cells and encased in an anodized flame-retardant aluminum alloy housing, "
                "it provides industry-leading thermal stability and resilience against thermal runaway. The battery pack boasts 65W bidirectional Power Delivery 3.0 via "
                "its primary USB-C port, supplemented by a secondary 30W USB-C port and an 18W USB-A QuickCharge output. An integrated monochromatic OLED display provides "
                "real-time readouts of remaining capacity percentage, operational output wattage, incoming charging voltage, and estimated time to full discharge under current load conditions."
            ),
            "how_to_use": (
                "To operate the Plasma Battery Pack efficiently, begin by fully charging the pack using a certified 65W USB-PD wall adapter. Plug the charger into "
                "the primary 'USB-C1 In/Out' port; the OLED display will illuminate showing input wattage and an incrementing percentage indicator until reaching 100%. "
                "To charge mobile workstations, tablets, or phones, simply connect your device's high-wattage charging cable to USB-C1 or USB-C2. The internal intelligent "
                "power-negotiation chip automatically identifies the connected device and supplies optimal voltage. For low-current peripherals like wireless earbuds or smart "
                "bands, double-tap the side control button to engage 'Trickle Charge Mode', preventing the power bank from auto-shutting off during trickle cycles. "
                "Single-click the power button at any time to inspect remaining cell capacity."
            ),
            "troubleshooting": (
                "In case of unexpected power behavior, follow these diagnostic procedures. Issue 1: Battery pack does not accept incoming charge or remains at 0%. "
                "Resolution: Inspect the USB-C cable for bent pins, verify the wall adapter delivers at least 15W of USB-PD power, and perform a master controller reset by "
                "holding the side power button down for 12 seconds. Issue 2: Output wattage is lower than device manufacturer rating. Resolution: Confirm you are plugged into "
                "the primary USB-C1 port and that your charging cable is rated for 5A/100W throughput. Issue 3: The OLED screen displays an 'OVERTEMP' error icon. "
                "Resolution: Immediately disconnect all connected devices, place the unit on a cool flat surface out of direct sunlight, and wait 20 minutes for temperatures to normalize."
            ),
            "warranty": (
                "The Plasma Battery Pack is warranted against manufacturing flaws, internal cell degradation exceeding 20% capacity drop, and short-circuit protection board "
                "failures for a period of 1 month (30 calendar days) from retail delivery. The 1-month warranty does not cover damages incurred through deep water submersion, "
                "structural crushing, disassembly of the aluminum casing, exposure to open flame, or use of substandard third-party chargers. For warranty service within the "
                "1-month period, contact our technical support division at support@agentichelpdesk.com with your original receipt and proof of device failure. Approved RMA requests "
                "qualify for direct replacement with an identical or superior capacity unit."
            )
        }
    },
    {
        "name": "Aether Router",
        "file_name": "aether_router_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$120.25",
        "model_no": "AR-7000-TRI",
        "sections": {
            "basic_info": (
                "The Aether Router is an ultra-fast, tri-band Wi-Fi 7 wireless networking hub engineered to satisfy high-density connected home and small office "
                "environments. Powered by a 2.0 GHz quad-core 64-bit processing unit and 1GB of DDR4 memory, it delivers aggregate theoretical wireless speeds of up to 9.6 Gbps "
                "across simultaneous 2.4 GHz, 5 GHz, and 6 GHz spectrum channels. The router features six external beamforming antennas with high-gain power amplifiers, "
                "one 10GbE WAN port for multigigabit fiber uplinks, four 2.5GbE LAN ports for low-latency wired connections, and full support for WPA3 Enterprise encryption. "
                "Its intelligent traffic orchestration engine automatically optimizes quality of service (QoS) for cloud gaming, 8K video streaming, and latency-critical VoIP calls."
            ),
            "how_to_use": (
                "Setting up your Aether Router requires just a few straightforward steps. First, position the router in a central, elevated location away from metal structures "
                "and thick concrete walls. Connect your broadband fiber terminal or modem to the yellow 10GbE WAN port using the provided Cat6a Ethernet cable. Plug in the 12V DC "
                "power adapter and push the power toggle; allow two minutes for the status indicator to turn solid sky blue. Connect your PC or mobile device to the default Wi-Fi "
                "network printed on the bottom label, or open a browser to '192.168.1.1'. The interactive QuickSetup Wizard will guide you through establishing a custom SSID, "
                "setting a strong WPA3 passphrase, and creating an isolated guest network for IoT devices."
            ),
            "troubleshooting": (
                "Should network connectivity issues arise, carry out the following troubleshooting protocols. Issue 1: WAN LED remains solid amber with no internet access. "
                "Resolution: Power cycle your fiber modem and the Aether Router in sequence, verify that the Ethernet cable is securely clicked into the WAN port, and confirm "
                "with your ISP whether MAC address cloning is required. Issue 2: Wireless dropouts or high interference on the 5GHz/6GHz bands. Resolution: Access the web admin "
                "portal, navigate to Wireless Settings, and enable Automatic Channel Selection (ACS) or change DFS channels to bypass local radar interference. Issue 3: Admin password "
                "lost or portal unreachable. Resolution: Use a paperclip to depress the recessed reset pinhole on the back panel for 10 seconds to restore factory default parameters."
            ),
            "warranty": (
                "The Aether Router includes a 1-month (30-day) manufacturer limited warranty starting on the date of original customer shipment. The warranty covers "
                "defects in router hardware components, integrated transceiver failure, Ethernet port solder defects, and bundled AC power adapter malfunctions. It explicitly "
                "excludes damage resulting from unauthorized third-party firmware flashing (e.g., non-certified OpenWrt builds), electrical surges caused by lightning, or physical "
                "antenna breakage due to impact. To submit a warranty claim within the 1-month term, email support@agentichelpdesk.com including your router serial number, MAC address, "
                "and a diagnostic system log snapshot for RMA evaluation."
            )
        }
    },
    {
        "name": "Nano-Sensors (100pk)",
        "file_name": "nano_sensors_100pk_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$89.99",
        "model_no": "NS-100-MEMS",
        "sections": {
            "basic_info": (
                "The Nano-Sensors (100pk) package delivers an industrial-grade array of one hundred miniaturized micro-electromechanical (MEMS) multi-sensor nodes. "
                "Engineered for comprehensive environmental monitoring, predictive equipment maintenance, structural health assessment, and distributed agricultural sensing, each thumbnail-sized node "
                "integrates precision sensors for temperature (-40°C to +125°C), relative humidity (0-100% RH), tri-axial acceleration, and localized magnetic flux. Nodes "
                "communicate via an ultra-low power Sub-GHz mesh wireless protocol capable of line-of-sight transmission up to 50 meters. Encased in IP67 water- and dust-resistant "
                "epoxy resin with pre-applied industrial thermal adhesive backing, each sensor incorporates an ambient energy-harvesting cell supported by a 3-year micro-battery reserve."
            ),
            "how_to_use": (
                "Deploying the Nano-Sensors array across your target monitoring zone is efficient and scalable. First, set up and power on the central Nano-Gateway receiver "
                "connected to your local network. Unpack the required number of sensor nodes from the anti-static packaging. Remove the pull-tab plastic insulator from the rear "
                "of each sensor to engage internal circuitry; a faint green micro-LED will flash once. Open the NanoMesh Gateway dashboard on your mobile device or terminal, "
                "and scan the individual 2D DataMatrix code on each node to register its unique telemetry ID and location tag. Peel off the protective adhesive film on the base "
                "and press the node firmly against the test surface for 10 seconds to ensure solid mechanical coupling for vibration sensing and thermal contact."
            ),
            "troubleshooting": (
                "In case of communication or telemetry irregularities, refer to the following guide. Issue 1: A registered node ceases transmitting telemetry to the gateway. "
                "Resolution: Check if the distance between the node and the nearest mesh neighbor exceeds 50 meters; install an intermediate repeater node or relocate the gateway "
                "to overcome thick concrete shielding. Issue 2: Sensor outputs irregular temperature or humidity spikes. Resolution: Inspect the protective membrane on the node "
                "aperture for oil, grease, or particulate clogging; clean gently using isopropyl alcohol and a lint-free swab. Issue 3: Gateway fails to recognize scanned node QR code. "
                "Resolution: Manually enter the 12-digit hex MAC ID printed beneath the barcode into the gateway's manual device registration portal."
            ),
            "warranty": (
                "The Nano-Sensors (100pk) is protected by a 1-month (30-day) limited replacement warranty covering factory component defects and dead-on-arrival (DOA) nodes. "
                "If any individual sensor node fails to initialize, negotiate mesh connectivity, or register accurate telemetry within 30 days of purchase, it will be replaced "
                "promptly upon verification. This 1-month warranty does not cover nodes subjected to mechanical crushing beyond 500 N, immersion in caustic chemical solvents, "
                "or intentional encapsulation stripping. For warranty claims, email support@agentichelpdesk.com with the affected sensor MAC IDs and a screenshot of the gateway's "
                "offline device log to receive replacement sensor hardware."
            )
        }
    },
    {
        "name": "Hyper-Drive SSD 2TB",
        "file_name": "hyper_drive_ssd_2tb_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$199.99",
        "model_no": "HD-2TB-NVME",
        "sections": {
            "basic_info": (
                "The Hyper-Drive SSD 2TB is a premier M.2 2280 NVMe solid-state drive built on PCIe 4.0 x4 architecture, designed for hardcore PC gamers, "
                "creative video editors, and machine learning practitioners who require blistering storage performance. Featuring cutting-edge 176-layer 3D TLC NAND "
                "flash coupled with a multi-core controller and 2GB of dedicated DDR4 DRAM cache, the drive achieves sequential read speeds up to 7,400 MB/s and "
                "sequential write speeds up to 6,800 MB/s. It comes equipped with an ultra-thin graphene thermal heat-spreader to mitigate thermal throttling under prolonged "
                "sustained workloads, and supports hardware-accelerated AES 256-bit encryption along with a formidable endurance rating of 1,200 Terabytes Written (TBW)."
            ),
            "how_to_use": (
                "Follow standard precautions when installing the Hyper-Drive SSD 2TB into your motherboard. First, shut down your desktop PC, disconnect the main AC power cord, "
                "and touch an unpainted metal surface to discharge static electricity. Locate the primary M.2 slot connected directly to the CPU PCIe lanes for maximum throughput. "
                "Carefully insert the drive at a 30-degree angle into the M.2 keyed slot until fully seated, then gently press down and secure it with the provided M.2 mounting screw "
                "or motherboard retention latch. Reassemble your PC and boot into the operating system. In Windows, open Disk Management (or 'fdisk / parted' in Linux), initialize "
                "the newly detected disk as GPT, and create an NTFS or ext4 partition to begin lightning-fast file operations."
            ),
            "troubleshooting": (
                "Consult the troubleshooting guide below to resolve storage detection or speed concerns. Issue 1: BIOS/UEFI or Windows does not recognize the SSD. "
                "Resolution: Ensure the drive is installed in an NVMe-capable slot rather than a legacy SATA-only M.2 slot, update your motherboard BIOS to the latest version, "
                "and verify storage controller settings are set to AHCI/NVMe rather than legacy IDE. Issue 2: Sequential transfer speeds test significantly below 7,000 MB/s. "
                "Resolution: Confirm the drive is running in PCIe 4.0 x4 mode rather than PCIe 3.0 x2 via CrystalDiskInfo or Hyper-Drive Utility. Issue 3: Drive reports high temperatures. "
                "Resolution: Ensure the motherboard M.2 thermal heatsink or included graphene pad makes complete contact with the controller chip."
            ),
            "warranty": (
                "The Hyper-Drive SSD 2TB includes a 1-month (30-day) limited hardware warranty valid from the confirmed delivery date. The warranty guarantees "
                "protection against NAND silicon failure, controller chip burnout, and firmware corruption under normal consumer workload patterns. The 1-month warranty "
                "is rendered void if the drive exceeds 100 TBW written within the initial 30 days (such as from continuous crypto-mining plots), or if the circuit board displays "
                "evidence of physical snapping, soldering modifications, or liquid contact. To initiate a warranty return within 1 month, contact support@agentichelpdesk.com "
                "with your invoice and a SMART diagnostic health screenshot for rapid RMA authorization."
            )
        }
    },
    {
        "name": "Sonic Screwdriver V2",
        "file_name": "sonic_screwdriver_v2_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$340.00",
        "model_no": "SS-V2-SONIC",
        "sections": {
            "basic_info": (
                "The Sonic Screwdriver V2 is a versatile multi-frequency acoustic resonance diagnostic tool and non-contact mechanical fastener manipulator "
                "designed for electronics engineers, hardware technicians, and advanced hobbyists. Featuring a wide-spectrum piezoelectric ultrasonic transducer capable "
                "of generating precise sound wave resonance between 20 Hz and 400 kHz, the device loosens, fastens, or analyzes micro-mechanical components without physical torque. "
                "Constructed from aerospace-grade brushed titanium with knurled ergonomic grips, it features a dual-stage activator button, a tactile haptic rotary frequency selector, "
                "an integrated high-lumen multi-spectrum LED targeting emitter, and a magnetic induction charging dock that replenishes the internal cell in under 40 minutes."
            ),
            "how_to_use": (
                "Using the Sonic Screwdriver V2 requires selecting the appropriate acoustic resonance mode for your workpiece. Lift the tool from its magnetic charging dock; "
                "the emitter ring will illuminate steady emerald. Rotate the knurled collar to choose your desired operating profile: Mode 1 for micro-fastener harmonic release, "
                "Mode 2 for acoustic density scanning, or Mode 3 for non-contact electromagnetic field detection. Aim the focused targeting LED at the target fastener or component "
                "from a distance of 2 to 5 centimeters. Depress the activator button halfway to focus the frequency lock; once the haptic feedback pulses twice, depress the button "
                "fully to emit the resonant wave burst until the fastener disengages or the diagnostic reading registers."
            ),
            "troubleshooting": (
                "If the tool fails to operate as expected, use these troubleshooting steps to diagnose the issue. Issue 1: Acoustic emitter does not vibrate or loosen fasteners. "
                "Resolution: Clean the emitter tip aperture using compressed air to remove microscopic debris, ensure the battery is charged above 30%, and adjust the rotary dial "
                "fine-tuning trim to match fastener resonance frequency. Issue 2: Targeting LED flashes amber with an audible warning tone. Resolution: The device has entered "
                "thermal safety lockout following excessive continuous firing; allow the tool to rest for 3 minutes to disperse internal transducer heat. Issue 3: Tool does not charge "
                "on magnetic dock. Resolution: Wipe the base gold pogo-pins with isopropyl alcohol to clear oxidation and ensure the dock is plugged into a 5V/2A power supply."
            ),
            "warranty": (
                "The Sonic Screwdriver V2 is covered by an official 1-month (30-day) limited warranty against defects in materials and manufacturing from the date of initial "
                "delivery. This warranty covers the ultrasonic transducer array, internal logic board, rotary selector mechanism, and magnetic charging base. It specifically excludes "
                "damage caused by using the tool as a physical pry bar, exposing the emitter tip to liquids, dropping the tool from heights exceeding one meter, or unauthorized casing "
                "disassembly. To file a warranty claim within the 1-month period, contact Helpdesk Support at support@agentichelpdesk.com with your order number and a brief video "
                "demonstrating the transducer failure to obtain replacement processing."
            )
        }
    },
    {
        "name": "Gravity Glove",
        "file_name": "gravity_glove_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$850.00",
        "model_no": "GG-850-FORCE",
        "sections": {
            "basic_info": (
                "The Gravity Glove is a state-of-the-art wearable localized gravitational and electromagnetic manipulation gauntlet engineered for industrial "
                "logistics, warehouse picking, and high-precision hazardous material handling. Integrating miniature localized gravimetric coil emitters across the palm "
                "and reinforced carbon-fiber articulated exoskeletal finger stabilizers, the glove allows operators to tether, attract, and manipulate objects weighing up "
                "to 5.0 kilograms from distances of up to 2.5 meters. Equipped with haptic force-feedback tendon actuators, the glove provides intuitive tactile resistance "
                "mimicking the exact weight and contour of the manipulated object. The glove is powered by a high-draw quick-swap lithium-graphene battery pack yielding 6 hours of continuous duty."
            ),
            "how_to_use": (
                "Before operating the Gravity Glove, ensure you are wearing safety goggles and standard work boots. Slide your hand into the glove gauntlet, ensuring each finger "
                "is comfortably aligned with the internal sensor channels, and cinch the dual Velcro wrist stabilizers firmly. Turn on the main power rocker switch located on the forearm "
                "cuff; the palm emitter will pulse in standby violet. Perform the 10-second motor calibration sequence by fully opening your hand, forming a fist, and pointing toward an "
                "open space. To attract an object, point your open palm directly at the target item within 2.5 meters, establish visual lock on the HUD crosshair, and slowly curl your index "
                "finger to generate localized attractive flux, pulling the item safely into your grasp."
            ),
            "troubleshooting": (
                "For unexpected behavior during gravimetric operation, follow these diagnostic steps. Issue 1: Palm attraction field is weak or fails to tether objects. "
                "Resolution: Ensure the target item weighs under the 5 kg threshold, clean the palm emitter lens with a microfiber cloth to prevent sensor obstruction, and confirm "
                "the battery pack has at least two illuminated charge bars. Issue 2: Finger haptic feedback feels locked or resists movement. Resolution: Press the emergency mechanical "
                "tension release lever on the wrist cuff to reset the servo spooling wires, then power-cycle the unit. Issue 3: Forearm warning buzzer sounds with flashing red LED. "
                "Resolution: The gravimetric induction coils have exceeded safe thermal limits; deactivate the glove immediately and allow 10 minutes for active fans to cool the coils."
            ),
            "warranty": (
                "The Gravity Glove is backed by a 1-month (30-day) limited industrial warranty covering defects in electronic controls, servo motors, flux emitter coils, and "
                "internal wiring harnesses from the date of verified delivery. The 1-month warranty does not cover fabric abrasion, tears resulting from sharp metal edges, "
                "water or chemical submersion, or coil burnout caused by attempting to lift objects exceeding the certified 5.0 kilogram limit. For warranty evaluation and return "
                "merchandise authorization within the 1-month window, email our specialized technical support team at support@agentichelpdesk.com with your serial number, "
                "purchase documentation, and error telemetry export."
            )
        }
    },
    {
        "name": "Smart Lens",
        "file_name": "smart_lens_manual.pdf",
        "category": "Electronics",
        "warranty_months": 1,
        "price": "$199.00",
        "model_no": "SL-199-HUD",
        "sections": {
            "basic_info": (
                "The Smart Lens is an advanced bio-compatible smart contact lens system featuring an embedded micro-OLED display capable of superimposing "
                "crisp augmented reality visual data directly onto the user's field of vision. Fabricated from medical-grade oxygen-permeable hydrogel polymer, each lens "
                "contains an ultra-dense 14,000 ppi micro-display, miniature eye-tracking sensors, a wireless RF power-harvesting loop, and an embedded intraocular pressure "
                "and glucose biometric sensor. The lens communicates wirelessly with an accompanying smart neckband or mobile handset via ultra-low-power near-field telemetry. "
                "Supplied with an inductive disinfection and wireless recharging travel case, the Smart Lens delivers seamless real-time heads-up navigation, messaging, and biometric health tracking."
            ),
            "how_to_use": (
                "Proper hygiene and careful handling are mandatory for the safe operation of the Smart Lens. Wash and thoroughly dry your hands with a lint-free towel "
                "before opening the smart disinfection charging case. Remove the lens using the soft-tipped silicone applicator tool, and inspect the hydrogel surface for debris. "
                "Place the lens gently onto the tip of your index finger, hold your eyelids open, and position the lens directly over your cornea, blinking softly until it seats "
                "comfortably. Put on the companion inductive neckband and power it on. Open the SmartLens mobile application to initiate the automated gaze calibration; glance at "
                "the four peripheral calibration beacons as prompted to calibrate touchless eye-tracking and blink gestures (double blink to select, long blink to return home)."
            ),
            "troubleshooting": (
                "If you experience visual display or connectivity issues, execute these troubleshooting protocols. Issue 1: Heads-up display is skewed, off-center, or blurry. "
                "Resolution: Gently close your eyes and massage the upper eyelid to re-center the lens over your pupil, or re-run the 30-second gaze calibration in the mobile application. "
                "Issue 2: The mobile application displays a 'Lens Disconnected' warning. Resolution: Ensure the companion smart neckband is placed properly around your neck within 20 cm "
                "of the lenses and check that the neckband battery is charged. Issue 3: Lens feels dry or uncomfortable during prolonged wear. Resolution: Apply 2 drops of certified "
                "sterile lubricating rewetting drops formulated for smart hydrogel contacts, or remove the lenses immediately if irritation persists."
            ),
            "warranty": (
                "The Smart Lens system is covered by a 1-month (30-day) limited hardware warranty from the original date of customer receipt. The 1-month warranty "
                "protects against electronic circuit defects, micro-OLED display line failure, wireless induction coil faults, and defects in the companion wireless charging case. "
                "Due to sanitary and health safety regulations, physical tears in the hydrogel membrane caused by fingernails, cosmetic damage from unapproved cleaning solutions, "
                "or lens loss are strictly excluded from warranty coverage. To submit a warranty claim within the 1-month term, contact support@agentichelpdesk.com with your "
                "order confirmation and diagnostic error logs from the SmartLens mobile app."
            )
        }
    }
]

def count_words(text):
    return len(re.findall(r'\b[a-zA-Z0-9\-\'\$]+\b', text))

def get_product_text(prod):
    return " ".join([
        prod['name'],
        "User Manual Official Technical Specification Operating Instructions Support Policy",
        "Category", prod['category'],
        "Retail Price", prod['price'],
        "Model Number", prod['model_no'],
        "Warranty Term", f"{prod['warranty_months']} Month Limited",
        "1. Product Overview & Technical Specifications",
        prod['sections']['basic_info'],
        "2. Setup & Operating Instructions",
        prod['sections']['how_to_use'],
        "3. Troubleshooting & Diagnostics Guide",
        prod['sections']['troubleshooting'],
        "4. Warranty Terms & Customer Support Information",
        "Warranty Summary:", f"{prod['warranty_months']} Month (30 Days) Limited Manufacturer Protection",
        prod['sections']['warranty']
    ])

def pad_to_500_words(prod):
    """Ensure the total text of the manual reaches exactly ~500-510 words."""
    current_count = count_words(get_product_text(prod))
    needed = 505 - current_count
    if needed > 0:
        # Add technical maintenance & compliance notes to warranty or troubleshooting
        supplement = (
            f" For technical assistance, scheduled firmware maintenance, compliance records, "
            f"and certified servicing documentation for the {prod['name']}, customers may access our verified "
            f"support repository 24/7 at https://helpdesk.internal/docs/{prod['model_no'].lower()}. "
            f"Ensure all service inquiries reference unit serial numbers to expedite processing."
        )
        words_supplement = re.findall(r'\b[a-zA-Z0-9\-\'\$]+\b', supplement)
        if len(words_supplement) > needed:
            # take needed words
            words_to_add = " " + " ".join(words_supplement[:needed]) + "."
        else:
            words_to_add = supplement
        prod['sections']['warranty'] += words_to_add

def build_pdf_manual(product, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    warranty_box_style = ParagraphStyle(
        'WarrantyBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1E3A8A')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(f"{product['name']} - User Manual", title_style))
    story.append(Paragraph("Official Technical Specification, Operating Instructions &amp; Support Policy", subtitle_style))

    # Meta Table (Specs / Attributes)
    meta_data = [
        [
            Paragraph("<b>Category:</b>", meta_label_style), Paragraph(product['category'], meta_val_style),
            Paragraph("<b>Retail Price:</b>", meta_label_style), Paragraph(product['price'], meta_val_style)
        ],
        [
            Paragraph("<b>Model Number:</b>", meta_label_style), Paragraph(product['model_no'], meta_val_style),
            Paragraph("<b>Warranty Term:</b>", meta_label_style), Paragraph(f"{product['warranty_months']} Month Limited", meta_val_style)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[90, 160, 90, 164])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Basic Product Information
    story.append(Paragraph("1. Product Overview &amp; Technical Specifications", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3B82F6"), spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(product['sections']['basic_info'], body_style))

    # Section 2: How to Use It
    story.append(Paragraph("2. Setup &amp; Operating Instructions", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3B82F6"), spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(product['sections']['how_to_use'], body_style))

    # Section 3: Troubleshooting Guide
    story.append(Paragraph("3. Troubleshooting &amp; Diagnostics Guide", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3B82F6"), spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(product['sections']['troubleshooting'], body_style))

    # Section 4: Warranty Information
    story.append(Paragraph("4. Warranty Terms &amp; Customer Support Information", section_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3B82F6"), spaceAfter=6, spaceBefore=0))
    
    # Styled Warranty Box Table
    warranty_table = Table(
        [[Paragraph(f"<b>Warranty Summary:</b> {product['warranty_months']} Month (30 Days) Limited Manufacturer Protection<br/><br/>{product['sections']['warranty']}", warranty_box_style)]],
        colWidths=[504]
    )
    warranty_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93C5FD')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(warranty_table)

    # Attach document title to canvas dynamically
    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.doc_title = f"{product['name']} User Manual"
        return c

    doc.build(story, canvasmaker=make_canvas)

def main():
    manuals_dir = os.path.join(os.path.dirname(__file__), "manuals")
    os.makedirs(manuals_dir, exist_ok=True)

    print(f"Generating manuals in: {manuals_dir}")
    print("=" * 70)

    for prod in PRODUCTS:
        # Ensure ~500-510 words
        pad_to_500_words(prod)
        total_text = get_product_text(prod)
        words = count_words(total_text)
        
        pdf_path = os.path.join(manuals_dir, prod['file_name'])
        build_pdf_manual(prod, pdf_path)
        file_size = os.path.getsize(pdf_path)
        
        print(f"[OK] {prod['name']:<24} -> {prod['file_name']:<30} | {words:>3} words | {file_size/1024:.1f} KB")

    print("=" * 70)
    print("All 10 product manuals successfully generated!")

if __name__ == "__main__":
    main()
