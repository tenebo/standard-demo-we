import os,network,networks
from modules import shared,ui_extra_networks
from modules.ui_extra_networks import quote_js
from ui_edit_user_metadata import LoraUserMetadataEditor
class ExtraNetworksPageLora(ui_extra_networks.ExtraNetworksPage):
	def __init__(A):super().__init__('Lora')
	def refresh(A):networks.list_available_networks()
	def create_item(D,name,index=None,enable_filter=True):
		H='prompt';I='sd_version';E=' + ';F='user_metadata';A=networks.available_networks.get(name);G,N=os.path.splitext(A.filename);L=A.get_alias();C={'name':name,'filename':A.filename,'shorthash':A.shorthash,'preview':D.find_preview(G),'description':D.find_description(G),'search_term':D.search_terms_from_path(A.filename)+' '+(A.hash or''),'local_preview':f"{G}.{shared.opts.samples_format}",'metadata':A.metadata,'sort_keys':{'default':index,**D.get_sort_keys(A.filename)},I:A.sd_version.name};D.read_user_metadata(C);J=C[F].get('activation text');K=C[F].get('preferred weight',.0);C[H]=quote_js(f"<lora:{L}:")+E+(str(K)if K else'opts.extra_networks_default_multiplier')+E+quote_js('>')
		if J:C[H]+=E+quote_js(' '+J)
		B=C[F].get('sd version')
		if B in network.SdVersion.__members__:C[I]=B;B=network.SdVersion[B]
		else:B=A.sd_version
		if shared.opts.lora_show_all or not enable_filter:0
		elif B==network.SdVersion.Unknown:
			M=network.SdVersion.SDXL if shared.sd_model.is_sdxl else network.SdVersion.SD2 if shared.sd_model.is_sd2 else network.SdVersion.SD1
			if M.name in shared.opts.lora_hide_unknown_for_versions:return
		elif shared.sd_model.is_sdxl and B!=network.SdVersion.SDXL:return
		elif shared.sd_model.is_sd2 and B!=network.SdVersion.SD2:return
		elif shared.sd_model.is_sd1 and B!=network.SdVersion.SD1:return
		return C
	def list_items(B):
		for(C,D)in enumerate(networks.available_networks):
			A=B.create_item(D,C)
			if A is not None:yield A
	def allowed_directories_for_previews(A):return[shared.cmd_opts.lora_dir,shared.cmd_opts.lyco_dir_backcompat]
	def create_user_metadata_editor(A,ui,tabname):return LoraUserMetadataEditor(ui,tabname,A)