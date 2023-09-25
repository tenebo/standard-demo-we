_A='ignore'
import importlib,logging,sys,warnings
from threading import Thread
from modules.timer import startup_timer
def imports():A='import torch';logging.getLogger('torch.distributed.nn').setLevel(logging.ERROR);logging.getLogger('xformers').addFilter(lambda record:'A matching Triton is not available'not in record.getMessage());import torch;startup_timer.record(A);import pytorch_lightning;startup_timer.record(A);warnings.filterwarnings(action=_A,category=DeprecationWarning,module='pytorch_lightning');warnings.filterwarnings(action=_A,category=UserWarning,module='torchvision');import gradio;startup_timer.record('import gradio');from modules import paths,timer,import_hook,errors;startup_timer.record('setup paths');import ldm.modules.encoders.modules;startup_timer.record('import ldm');import sgm.modules.encoders.modules;startup_timer.record('import sgm');from modules import shared_init as B;B.initialize();startup_timer.record('initialize shared');from modules import processing,gradio_extensons,ui;startup_timer.record('other imports')
def check_versions():
	from modules.shared_cmd_options import cmd_opts as A
	if not A.skip_version_check:from modules import errors as B;B.check_versions()
def initialize():from modules import initialize_util as A;A.fix_torch_version();A.fix_asyncio_event_loop_policy();A.validate_tls_options();A.configure_sigint_handler();A.configure_opts_onchange();from modules import modelloader as C;C.cleanup_models();from modules import sd_models as D;D.setup_model();startup_timer.record('setup SD model');from modules.shared_cmd_options import cmd_opts as B;from modules import codeformer_model as E;warnings.filterwarnings(action=_A,category=UserWarning,module='torchvision.transforms.functional_tensor');E.setup_model(B.codeformer_models_path);startup_timer.record('setup codeformer');from modules import gfpgan_model as F;F.setup_model(B.gfpgan_models_path);startup_timer.record('setup gfpgan');initialize_rest(reload_script_modules=False)
def initialize_rest(*,reload_script_modules=False):
	'\n    Called both from initialize() and when reloading the ourui.\n    ';from modules.shared_cmd_options import cmd_opts as B;from modules import sd_samplers as G;G.set_samplers();startup_timer.record('set samplers');from modules import extensions as H;H.list_extensions();startup_timer.record('list extensions');from modules import initialize_util as I;I.restore_config_state_file();startup_timer.record('restore config state file');from modules import shared as C,upscaler as J,scripts as D
	if B.ui_debug_mode:C.sd_upscalers=J.UpscalerLanczos().scalers;D.load_scripts();return
	from modules import sd_models as K;K.list_models();startup_timer.record('list SD models');from modules import localization as L;L.list_localizations(B.localizations_dir);startup_timer.record('list localizations')
	with startup_timer.subcategory('load scripts'):D.load_scripts()
	if reload_script_modules:
		for M in[B for(A,B)in sys.modules.items()if A.startswith('modules.ui')]:importlib.reload(M)
		startup_timer.record('reload script modules')
	from modules import modelloader as N;N.load_upscalers();startup_timer.record('load upscalers');from modules import sd_vae as O;O.refresh_vae_list();startup_timer.record('refresh VAE');from modules import textual_inversion as P;P.textual_inversion.list_textual_inversion_templates();startup_timer.record('refresh textual inversion templates');from modules import script_callbacks as Q,sd_hijack_optimizations as R,sd_hijack as A;Q.on_list_optimizers(R.list_optimizers);A.list_optimizers();startup_timer.record('scripts list_optimizers');from modules import sd_unet as S;S.list_unets();startup_timer.record('scripts list_unets')
	def T():
		"\n        Accesses shared.sd_model property to load model.\n        After it's available, if it has been loaded before this access by some extension,\n        its optimization may be None because the list of optimizaers has neet been filled\n        by that time, so we apply optimization again.\n        ";C.sd_model
		if A.current_optimizer is None:A.apply_optimizations()
		from modules import devices as B;B.first_time_calculation()
	Thread(target=T).start();from modules import shared_items as U;U.reload_hypernetworks();startup_timer.record('reload hypernetworks');from modules import ui_extra_networks as E;E.initialize();E.register_default_pages();from modules import extra_networks as F;F.initialize();F.register_default_extra_networks();startup_timer.record('initialize extra networks')