#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket::INET;
use Time::HiRes qw(usleep);
use POSIX qw(strftime);
use IO::Handle;
use Cwd;
use Win32;
use Win32::GUI;

my ($freq_start, $freq_end, $freq_step);

# The next sections build up the application window.
my $main = Win32::GUI::Window->new(
	-name => 'Main',
	-text => 'Frequency Scanner',
	-width => 280,
	-height => 260,
    -dialogui => 1,
);

my $font = Win32::GUI::Font->new(
	-name => "Garamond", -size => 12, -foreground => [294,229,255],
);

my $font1 = Win32::GUI::Font->new(
	-name => "Garamond", -size => 12, -bold => 0, -italic => 0,
);

my $font2 = Win32::GUI::Font->new(
	-name => "Garamond", -size => 12, -bold => 1, -italic => 1,	-underline => 1,
);

$main->AddButton(
    -name => "Cancel", -text => "Cancel", -pos  => [60, 175], -background => [255,0,0],
);

$main->AddButton(
    -name => "Proceed", -text => "Proceed", -pos  => [160, 175], -background => [125,218,88],
);

$main->AddLabel(
	-name => "lbl1", -text => "Radio QRG SWEEP", -font => $font2, -left => 60, -top  => 12,	-foreground => [109,0,255],
);

$main->AddLabel(
	-name => "lbl2", -text => "Start QRG: ", -font => $font1, -left => 39, -top  => 42,
);

my $txtStart = $main->AddTextfield(
	-name => "txtStart", -left => 112, -top  => 42, -size => [60, 20], -align => "center", -tabstop => 1,
);
$txtStart->Text("7000000");
$main->AddLabel(
	-name => "lbl5", -text => "Hz", -font => $font1, -left => 175, -top  => 42,
);

$main->AddLabel(
	-name => "lbl3", -text => "Stop QRG: ", -font => $font1, -left => 39, -top  => 82,
);

my $txtStop = $main->AddTextfield(
	-name => "txtStop", -left => 112, -top  => 82, -size => [60, 20], -align => "center", -tabstop => 1,
);
$txtStop->Text("7040000");
$main->AddLabel(
	-name => "lbl6", -text => "Hz", -font => $font1, -left => 175, -top  => 82,
);

$main->AddLabel(
	-name => "lbl4", -text => "QRG Step: ", -font => $font1, -left => 59, -top  => 122,
);

my $txtStep = $main->AddTextfield(
	-name => "txtStop", -left => 132, -top  => 122, -size => [40, 20], -align => "center", -tabstop => 1,
);
$txtStep->Text("250");
$main->AddLabel(
	-name => "lbl7", -text => "Hz", -font => $font1, -left => 175, -top  => 122,
);

$main->Center;
$main->Show();
$main->txtStart->SetFocus;
Win32::GUI::Dialog();

sub Main_Terminate {
	-1;
}

sub Cancel_Click {
    exit 0;
}

sub Proceed_Click {
    $freq_start = $txtStart->Text();    
	$freq_end   = $txtStop->Text();
	$freq_step  = $txtStep->Text();

    return -1;
}

# ============================================================
# USER SETTINGS (easy to edit)
# ============================================================
#my $freq_start      = 14000000;     # Hz
#my $freq_end        = 14350000;     # Hz
#my $freq_step       = 250;        # Hz

my $base_dwell_ms   = 200;         # normal dwell time
my $boost_dwell_ms  = 600;         # dwell time when signal strong
my $boost_threshold = -80;         # S-meter threshold for longer dwell

my $s_samples       = 3;           # number of S-meter samples per freq
my $s_interval_ms   = 50;          # time between samples

my $rig_host        = "localhost";
my $rig_port        = 4532;

my $log_dir         = ".";         # directory for CSV logs

# Autoflush STDOUT for interactive prompts
$| = 1;

# ============================================================
# FUNCTION: open a daily CSV log file
# ============================================================
my $current_date = "";
my $CSV;

sub open_sweep_log {
    # Create a unique filename for each sweep
    my $timestamp = strftime("%Y-%m-%d_%H-%M-%S", localtime);
    my $filename = "$log_dir/scan_$timestamp.csv";

    open($CSV, ">", $filename) or die "Cannot open $filename: $!";
    
    # Write header
    print $CSV "timestamp,freq_hz,s_meter\n";
    $CSV->flush();

    return $filename;   # return the filename so Python can archive it later
}

# ============================================================
# FUNCTION: log a CSV line
# ============================================================
sub csv_log {
    my ($freq, $s) = @_;
    my $ts = strftime("%Y-%m-%d %H:%M:%S", localtime);
    print $CSV "$ts,$freq,$s"; #Removed '\n' at the end.
    $CSV->flush();   # <-- this is the missing piece
}

# ============================================================
# FUNCTION: send command to rigctld
# ============================================================
sub rig_cmd {
    my ($cmd) = @_;

    my $sock = IO::Socket::INET->new(
        PeerAddr => $rig_host,
        PeerPort => $rig_port,
        Proto    => 'tcp',
        Timeout  => 1,
    );

    return undef unless $sock;

    print $sock "$cmd\n";
    my $resp = <$sock>;
    close $sock;

    return $resp;
}

# ============================================================
# CLEAN EXIT HANDLER
# ============================================================
$SIG{INT} = sub {
    print "\nExiting cleanly...\n";
    close $CSV if $CSV;
    exit 0;
};

print "Scanner started...\n";

# Pre-calc number of steps for progress indicator
my $total_steps = int(($freq_end - $freq_start) / $freq_step) + 1;

# ============================================================
# MAIN SCAN LOOP (with progress indicator + per-sweep logs)
# ============================================================
while (1) {

    # --------------------------------------------------------
    # OPEN A NEW CSV FILE FOR THIS SWEEP
    # --------------------------------------------------------
    my $csv_file = open_sweep_log();

    my $step = 0;

    for (my $freq = $freq_start; $freq <= $freq_end; $freq += $freq_step) {

        $step++;
        my $percent = int(($step / $total_steps) * 100);

        print "\rScanning $freq Hz  [$percent%]   ";

        rig_cmd("F $freq");

        # PEAK S-METER READINGS
		my $peak = undef;

		for (1 .. $s_samples) {
    		my $s = rig_cmd("l STRENGTH");
    		if (defined $s && $s =~ /^-?\d+/) {
        		if (!defined $peak || $s > $peak) {
            		$peak = $s;
        		}
    		}
   		usleep($s_interval_ms * 1000);
		}

		my $peak_s = defined $peak ? $peak : "ERR";

        # Log to CSV
        csv_log($freq, $peak_s);

		if ($peak_s ne "ERR" && $peak_s > $boost_threshold) {
    		usleep($boost_dwell_ms * 1000);
		} else {
    		usleep($base_dwell_ms * 1000);
		}
    }

    print "\nSweep complete. Run again (y/n): ";

    close $CSV;   # <-- CLOSE THE SWEEP FILE HERE

    select(undef, undef, undef, 0.1);

    my $ans = <STDIN>;
    chomp($ans);
    $ans = lc($ans);

    if ($ans ne 'y') {
        system("\"C:\\Users\\g4fkh\\AppData\\Local\\Python\\Pythoncore-3.14-64\\python.exe\" \"C:\\Radio\\Perl_Apps\\Scanner\\plot_sweep.py\"");
        print "Exiting scanner...\n";
        exit 0;
    }

    chdir "C:/Radio/Perl_Apps/Scanner" or die "Cannot chdir: $!";
    system("\"C:\\Users\\g4fkh\\AppData\\Local\\Python\\Pythoncore-3.14-64\\python.exe\" \"C:\\Radio\\Perl_Apps\\Scanner\\plot_sweep.py\"");

    print "Starting next sweep...\n";
}